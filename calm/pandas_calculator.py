import numpy

class PandasCalculator(object):
    """docstring for PandasCalculator"""
    def __init__(self):
        super(PandasCalculator, self).__init__()

    def median(self, pandas_series):
        return pandas_series.series.median()

    def mean(self, pandas_series):
        return pandas_series.series.mean()

    def sum(self, pandas_series):
        return pandas_series.series.sum()

    def square_diff(self, pandas_series1, pandas_series2):
        new_ps = pandas_series1.make_copy()
        new_ps.series = (pandas_series1.series - pandas_series2.series)**2
        return new_ps

    def abs_diff(self, pandas_series1, pandas_series2):
        new_ps = pandas_series1.make_copy()
        diff_ts = (pandas_series1.series - pandas_series2.series)
        new_ps.series = diff_ts.abs()
        return new_ps

    def min(self, pandas_series):
        return pandas_series.series.min()

    def argmin(self, pandas_series):
        return pandas_series.series.argmin()

    def scalar_log10(self, scalar):
        return numpy.log10(scalar)
