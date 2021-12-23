#!/usr/bin/env python3

import sys
import argparse
import datetime

from tools import groupBy
from hdr_manipulation import (
    loadHdrSlices,
    timestampToDate,
    sliceStartTimestamp,
    sliceEndTimestamp,
    slicesStartTimestamp,
    slicesEndTimestamp,
    slicesCountNonempty,
    slicesMinValue,
    slicesMaxValue,
    sliceValueCount,
    slicesValueCount,
    aggregateSlices,
    normalizedDistribution,
    histogramGetValueAtPercentile,
)
from output_handling import (
    canCreateFile,
    plotToFigure,
    plotToDatafile,
)

# constants
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
SIGNIFICANT_FIGURES = 3
MAX_PERCENTILE_REACHED = 99.75
PLOT_POINTS_COUNT = 500


if __name__ == '__main__':
    # cmdline parsing
    parser = argparse.ArgumentParser(
        description='Manipulate HDR data generated in NoSQLBench.'
    )
    parser.add_argument('filename', help='HDR input data')
    parser.add_argument('-i', '--inspect', help='Detailed input breakdown', action='store_true')
    #
    aParserGroup = parser.add_argument_group('Analysis tasks')
    aParserGroup.add_argument('-m', '--metric', metavar='METRICTAG', nargs=1, help='Work on the specified metric tag (interactive choice if not provided)')
    aParserGroup.add_argument('-b', '--baseplot', action='store_true', help='Create standard distribution plot')
    aParserGroup.add_argument('-c', '--percentiles', action='store_true', help='Create percentile analysis')
    aParserGroup.add_argument('-s', '--stability', action='store_true', help='Perform stability analysis (per-slice plots)')
    #
    oParserGroup = parser.add_argument_group('Output control')
    oParserGroup.add_argument('-p', '--plot', metavar='PLOTFILEROOT', nargs=1, help='Create plot images (with given file root)')
    oParserGroup.add_argument('-d', '--dump', metavar='DUMPFILEROOT', nargs=1, help='Dump to data files (with given file root)')
    oParserGroup.add_argument('-f', '--force', action='store_true', help='Overwrite existing file(s) if necessary')
    #
    args = parser.parse_args()

    # sanity checks
    if not args.baseplot and not args.percentiles and not args.stability:
        print('WARNING: Nothing to do.\n')
        parser.print_help()
        sys.exit(0)
    if args.plot is None and args.dump is None:
        print('WARNING: No output mode(s) provided.\n')
        parser.print_help()
        sys.exit(0)

    # pre-read the log in its entirety
    # get histograms from the log file, grouping by tag
    slicesByTag = {
        t: sorted(
            sls,
            key=sliceStartTimestamp,
        )
        for t, sls in groupBy(
            loadHdrSlices(args.filename),
            keyer=lambda sl: sl.tag,
        ).items()
    }
    # All timestamps and durations in this routine are in MILLISECONDS
    t0 = min(slicesStartTimestamp(sls) for sls in slicesByTag.values())
    date0 = timestampToDate(t0)
    t1 = max(slicesEndTimestamp(sls) for sls in slicesByTag.values())
    date1 = timestampToDate(t1)

    # detailed input breakdown if required
    if args.inspect:
        print('HDR log details for "%s"' % args.filename)
        print('  Start time: %s' % date0.strftime(DATE_FORMAT))
        print('  End time:   %s' % date1.strftime(DATE_FORMAT))
        print('  Time interval covered: %i ms' % (t1-t0))
        print('    (time refs below are relative to "Start time")')
        print('  Tags (%i total):' % len(slicesByTag))
        for tag, slices in sorted(slicesByTag.items()):
            print('    Tag "%s", %i slices.' % (
                tag,
                len(slices),
            ))
            # per-tag metrics
            tagValues = slicesValueCount(slices)
            tagMax = slicesMaxValue(slices)
            tagMin = slicesMinValue(slices)
            tagT0 = slicesStartTimestamp(slices)
            tagT1 = slicesEndTimestamp(slices)
            print('      Values: %i (ranging %.2f to %.2f ms)' % (
                tagValues,
                tagMin,
                tagMax,
            ))
            print('      Time interval: %6i to %6i (%6i ms total)' % (
                tagT0-t0,
                tagT1-t0,
                tagT1-tagT0,
            ))
            print('      Slices:')
            #
            for sli, sl in enumerate(slices):
                print('        (%3i) %12i vals, t = %6i to %6i (%6i ms)' % (
                    sli,
                    sliceValueCount(sl),
                    sliceStartTimestamp(sl) - t0,
                    sliceEndTimestamp(sl) - t0,
                    sliceEndTimestamp(sl) - sliceStartTimestamp(sl),
                ))

    # ensure a metric is chosen
    if args.metric is None:
        print('Available metrics to analyse:')
        availableMetrics = sorted(slicesByTag.keys())
        print('\n'.join(
            '  (%2i) %52s (%2i non-empty slices, %9i values, covers %6i ms)' % (
                mi,
                '"%s"' % m,
                slicesCountNonempty(slicesByTag[m]),
                slicesValueCount(slicesByTag[m]),
                slicesEndTimestamp(slicesByTag[m]) - slicesStartTimestamp(slicesByTag[m]),
            )
            for mi, m in enumerate(availableMetrics)
        ))
        mIndex = int(input('Please choose a metric index (0-%i): ' % (len(slicesByTag)-1)))
        metricName = availableMetrics[mIndex]
    else:
        metricName = args.metric[0]

    # start producing material for the plots
    plotDataMap = {}

    # common assessments
    fullHistogram = aggregateSlices(slicesByTag[metricName], SIGNIFICANT_FIGURES)
    maxX = histogramGetValueAtPercentile(fullHistogram, MAX_PERCENTILE_REACHED)
    xStep = maxX / PLOT_POINTS_COUNT

    # ordinary distribution of the target metric ("baseplot")
    if args.baseplot:
        print('  * Calculating base plot ... ', end='')
        xs, ys = normalizedDistribution(
            fullHistogram,
            xStep,
            MAX_PERCENTILE_REACHED,
        )
        plotDataMap['baseplot'] = [(xs, ys)]
        print('done.')

    # per-slice plots
    if args.stability:
        if len(slicesByTag[metricName]) > 1:
            print('  * Calculating stability plot ... ', end='')
            perSlicePlots0 = [
                normalizedDistribution(
                    sl,
                    xStep,
                    MAX_PERCENTILE_REACHED,
                )
                for sl in slicesByTag[metricName]
            ]
            # we need to pad this with additional trailing zeroes
            # and have the same xs for all curves
            fullXs = max([pl[0] for pl in perSlicePlots0], key=len)
            perSlicePlots = [
                (fullXs, ys + [0] * (len(fullXs) - len(ys)))
                for xs, ys in perSlicePlots0
            ]
            #
            plotDataMap['stability'] = perSlicePlots
            print('done.')
        else:
            print('*WARNING*: Nothing to plot for stability analysis.')

    # percentile diagram (a.k.a. integral of the base plot)
    if args.percentiles:
        print('  * Calculating percentile plot ... ', end='')
        if 'baseplot' in plotDataMap:
            bxs, bys = plotDataMap['baseplot'][0]
        else:
            # we need the base plot if not calculated yet
            bxs, bys = normalizedDistribution(
                fullHistogram,
                xStep,
                MAX_PERCENTILE_REACHED,
            )
        #
        pys = bxs
        from functools import reduce
        pxs0 = reduce(
            lambda ac, newval: (ac[0]+newval, ac[1]+[ac[0]+newval]),
            bys,
            (0, []),
        )[1]
        pxs = [x * xStep * 100 for x in pxs0]
        plotDataMap['percentiles'] = [(pxs, pys)]
        print('done.')

    # Output of curves calculated so far
    for plotK, plotData in sorted(plotDataMap.items()):
        print('  * Output for "%s": ' % plotK)
        if args.plot:
            fileName = '%s_%s.%s' % (args.plot[0], plotK, 'png')
            if canCreateFile(fileName, args.force):
                if plotToFigure(plotK, plotData, xStep, metricName, fileName):
                    print('      %s' % fileName)
                else:
                    print('      *FAILED*: %s' % fileName)
            else:
                print('      *SKIPPING*: %s' % fileName)
        if args.dump:
            fileName = '%s_%s.%s' % (args.dump[0], plotK, 'dat')
            if canCreateFile(fileName, args.force):
                if plotToDatafile(plotK, plotData, xStep, metricName, fileName):
                    print('      %s' % fileName)
                else:
                    print('      *FAILED*: %s' % fileName)
            else:
                print('      *SKIPPING*: %s' % fileName)

