import numpy
import pandas

class PandasTimeSeries(object):
    """docstring for PandasTimeSeries"""
    def __init__(self):
        super(PandasTimeSeries, self).__init__()
        self.series = None

    def __len__(self):
        return len(self.series)

    def __str__(self):
        return str(self.series)

    def load_csv(self, csv_path):
        self.series = pandas.read_csv(csv_path, index_col=0, header=None,
                                           squeeze=True)

    def write_csv(self, csv_path):
        self.series.to_csv(csv_path, header=False)

    def load_npy_arrays(self, time_array, signal_array):
        self.series = pandas.Series(signal_array, index=time_array)

    def make_copy(self):
        my_copy = PandasTimeSeries()
        my_copy.series = self.series.copy()
        return my_copy

    def set_signal_values_from_npy_array(self, signal_array):
        new_series = pandas.Series(signal_array, index=self.series.index)
        self.series = new_series

    def set_signal_from_scalar(self, scalar, index_list=None):
        if index_list is None:
            self.series.fill(scalar)
        elif len(index_list) > 0:
            scalar_list = [scalar] * len(index_list)
            self.set_values_at_indices(scalar_list, index_list)
        else:
            return

    def sum_signal_with_array(self, signal_array):
        self.series += signal_array

    def is_similar_to(self, other_time_series, atol=1e-1):
        return numpy.allclose(self.series, other_time_series.series, atol=atol)

    def get_values_at_indices(self, index_list):
        sub_series = self.series.ix[index_list]
        sub_ts = PandasTimeSeries()
        sub_ts.series = sub_series
        return sub_ts

    def set_values_at_indices(self, new_values, index_list):
        self.series.ix[index_list] = new_values

    def isfinite(self):
        return numpy.isfinite(self.series).all()

    def get_indices_where_geq(self, threshold):
        bool_series = (self.series >= threshold)
        series_where_true = self.series[bool_series]
        inds = series_where_true.index
        return inds

    def get_indices_where_lt(self, threshold):
        bool_series = (self.series < threshold)
        series_where_true = self.series[bool_series]
        inds = series_where_true.index
        return inds
