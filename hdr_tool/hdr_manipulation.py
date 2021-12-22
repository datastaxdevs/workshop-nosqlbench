""" hdr_manipulation.py
        In particular, all time unit conversion happen
        in this module, which must then respect a contract
        to always return consistent units (viz. msec for all quantities)
"""

import datetime
from functools import reduce
from hdrh.log import HistogramLogReader
from hdrh.histogram import HdrHistogram

# CONSTANTS
# 'values' stored in histograms are in ns, we need ms
VALUE_FACTOR = 1.0e6


# Loader
def loadHdrSlices(filename):
    slices = []    
    baseHistogram = None
    lReader = HistogramLogReader(filename, baseHistogram)
    while True:
        tSlice = lReader.get_next_interval_histogram()
        if tSlice is None:
            break
        else:
            slices.append(tSlice)
    #
    return slices


# Single-slice functions
def sliceStartTimestamp(slice):
    return slice.start_time_stamp_msec


def sliceEndTimestamp(slice):
    return slice.end_time_stamp_msec


def sliceMaxValue(slice):
    return slice.max_value / VALUE_FACTOR


def sliceMinValue(slice):
    return slice.min_value / VALUE_FACTOR


def sliceValueCount(slice):
    return slice.total_count


# Slice-list functions
def slicesStartTimestamp(slices):
    earliestMsec = min(sliceStartTimestamp(sl) for sl in slices)
    return earliestMsec


def slicesEndTimestamp(slices):
    earliestMsec = max(sliceEndTimestamp(sl) for sl in slices)
    return earliestMsec


def slicesMinValue(slices):
    return min(sliceMinValue(sl) for sl in slices)


def slicesMaxValue(slices):
    return max(sliceMaxValue(sl) for sl in slices)


def slicesCountNonempty(slices):
    return sum(
        1 if sliceValueCount(sl) > 0 else 0
        for sl in slices
    )


def slicesValueCount(slices):
    return sum(sliceValueCount(sl) for sl in slices)


# Utilities
def timestampToDate(tstamp):
    return datetime.datetime.fromtimestamp(tstamp / 1000.0)


def aggregateSlices(slices, sigFigures):
    metricMax = slicesMaxValue(slices)
    fullHistogram = HdrHistogram(1, int(1+ metricMax*VALUE_FACTOR), sigFigures)
    reduce(lambda _, b: fullHistogram.add(b), slices, None)
    return fullHistogram


# Histogram functions
def histogramGetValueAtPercentile(histogram, percentile):
    # in the histogram we have ns, we want to make them into ms
    return  histogram.get_value_at_percentile(percentile) / VALUE_FACTOR


# Extraction for plots
def normalizedDistribution(histogram, x_incr, max_percentile):
    # NOTE: x_incr is expected to be passed in ms
    x_incr_ns = x_incr * VALUE_FACTOR
    if sliceValueCount(histogram) > 0:
        cursor = histogram.get_linear_iterator(value_units_per_bucket=x_incr_ns)
        xs0, ys0 = zip(*(
            (
                0.5 * (step.value_iterated_from + step.value_iterated_to),
                step.count_added_in_this_iter_step,
            )
            for step in cursor
            if step.percentile <= max_percentile
        ))
        #
        xs = [x / VALUE_FACTOR for x in xs0]
        # integral must be == 1 for ease of comparisons:
        ys = [y / (histogram.total_count * x_incr) for y in ys0]
        #
        return xs, ys
    else:
        return [], []