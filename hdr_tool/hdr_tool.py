#!/usr/bin/env python

import argparse
from hdrh.log import HistogramLogReader


if __name__ == '__main__':
    # cmdline parsing
    parser = argparse.ArgumentParser(
        description='Manipulate HDR data from NoSQLBench.'
    )
    parser.add_argument('filename', help='HDR input data')
    parser.add_argument('-i', '--inspect', help='Detailed input breakdown', action='store_true')
    parser.add_argument('-m', '--metric', metavar='METRICTAG', nargs=1, help='Work on the specified metric tag (interactive choice if not provided)')

    parser.add_argument('-b', '--baseplot', action='store_true', help='Create standard plot')
    parser.add_argument('-c', '--percentiles', action='store_true', help='Percentile analysis')
    parser.add_argument('-s', '--stability', action='store_true', help='Stability analysis (first vs. last third of slices)')

    parser.add_argument('-p', '--plot', metavar='PLOTFILEROOT', nargs=1, help='Create plot images (with given file root)')
    parser.add_argument('-d', '--dump', metavar='DUMPFILEROOT', nargs=1, help='Dump to data files (with given file root)')
    parser.add_argument('-f', '--force', action='store_true', help='Overwrite existing file(s) if necessary')
    args = parser.parse_args()

    print(args)