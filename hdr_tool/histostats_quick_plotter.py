#!/usr/bin/env python3

import sys
import os
import argparse

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None

from tools import groupBy
from output_handling import plotHistostats, canCreateFile


##

TAG_PREFIX = 'Tag='
FIXED_LEGEND = ['Tag', 'Interval_Start', 'Interval_Length', 'count']
COMMENT_CHAR = '#'
# interval start/length are in seconds, we want them in ms
DURATIONS_FACTOR = 1.0e-3
# Max/min and percentiles are in nanoseconds, we want them in ms
VALUE_FACTOR = 1.0e6

def _parseFrame(line, legend):
    if line[:len(TAG_PREFIX)] != TAG_PREFIX:
        raise ValueError('Malformed data line found (%s)' % line)
    pieces = [p.strip() for p in line.split(',')]
    if len(pieces) != len(legend) + 4:
        raise ValueError('Legend/data line mismatch (%s)' % line)
    else:
        # fixed part. We bring everything to milliseconds here
        tag = pieces[0][len(TAG_PREFIX):]
        start = float(pieces[1]) / DURATIONS_FACTOR
        duration = float(pieces[2]) / DURATIONS_FACTOR
        end = start + duration
        count = int(pieces[3])
        # legend-part. We bring everything to milliseconds here
        valueMap = {
            leg: float(pie) / VALUE_FACTOR
            for leg, pie in zip(legend, pieces[len(FIXED_LEGEND):])
        }
        #
        return {
            'tag': tag,
            'start': start,
            'duration': duration,
            'end': end,
            'count': count,
            'values': valueMap,
        }


def loadHistostats(filename):
    # we expect this to well fit in memory:
    headers = []
    lines = []
    for _line in open(filename).readlines():
        line = _line.strip()
        if line != '':
            if line[0] == COMMENT_CHAR:
                headers += [line]
            else:
                lines += [line]
    #
    if headers == []:
        raise ValueError('No headers in file')
    else:
        legend0 = [
            p.strip()
            for p in headers[-1][1:].split(',')
        ]
        if any([
            lExp != lFound
            for lExp, lFound in zip(
                legend0[:len(FIXED_LEGEND)],
                FIXED_LEGEND,
            )
        ]):
            raise ValueError('Unexpected legend in file (%s)' % headers[-1])
        else:
            legend = legend0[len(FIXED_LEGEND):]
            # let us parse the lines containing data
            frames = [
                _parseFrame(l, legend)
                for l in lines
            ]
            return frames, legend

##


if __name__ == '__main__':
    # cmdline parsing
    parser = argparse.ArgumentParser(
        description='Quickly plot "--log-histostats" output from NoSQLBench to an image.'
    )
    parser.add_argument('filename', help='Histostats input file')
    parser.add_argument('-m', '--metric', metavar='METRICTAG', nargs=1, help='Work on the specified metric tag (interactive choice if not provided)')
    parser.add_argument('-p', '--plot', metavar='PLOTFILEROOT', nargs=1, help='Create plot image (with given file root), automatic if not provided')
    parser.add_argument('--include-max', action='store_true', help='Include "max" to plotting', default=False)
    parser.add_argument('-f', '--force', action='store_true', help='Overwrite existing file if necessary')
    #
    args = parser.parse_args()

    # load the provided file
    loadedFrames, legend = loadHistostats(args.filename)
    framesByTag = {
        tag: sorted(
            frames,
            key=lambda f: f['start'],
        )
        for tag, frames in groupBy(
            loadedFrames,
            keyer=lambda fr: fr['tag'],
        ).items()
    }
    
    # ensure a metric is chosen
    if args.metric is None:
        print('Available metrics to analyse:')
        availableMetrics = sorted(framesByTag.keys())
        print('\n'.join(
            '  (%2i) %52s (%2i non-empty frames, %9i values, covers %6i ms)' % (
                mi,
                '"%s"' % m,
                len([f for f in framesByTag[m] if f['count'] > 0]),
                sum([f['count'] for f in framesByTag[m]]),
                (
                    max([f['end'] for f in framesByTag[m]]) \
                    - min([f['start'] for f in framesByTag[m]])
                ),
            )
            for mi, m in enumerate(availableMetrics)
        ))
        mIndex = int(input('Please choose a metric index (0-%i): ' % (len(framesByTag)-1)))
        metricName = availableMetrics[mIndex]
    else:
        metricName = args.metric[0]

    if args.plot is None:
        plotRoot = os.path.splitext(os.path.basename(args.filename))[0]
    else:
        plotRoot = args.plot[0]

    # prepare the plot data
    frames = framesByTag[metricName]
    if frames == []:
        raise ValueError('Nothing to plot')
    else:
        plotX = [
            frame[pos]
            for frame in frames
            for pos in ['start', 'end']
        ]
        values = {
            curve: [
                frame['values'][curve]
                for frame in frames
                for _ in range(2)
            ]
            for curve in legend
            if curve != 'max' or args.include_max
        }
        #
        fileName = '%s.%s' % (plotRoot, 'png')
        if canCreateFile(fileName, args.force):
            if plotHistostats(plotX, values, legend, metricName, fileName):
                print('      %s' % fileName)
            else:
                print('      *FAILED*: %s' % fileName)
        else:
            print('      *SKIPPING*: %s' % fileName)
