import pandas

class PandasTimeSeries(object):
    """docstring for PandasTimeSeries"""
    def __init__(self):
        super(PandasTimeSeries, self).__init__()
        self.time_series = None

    def __len__(self):
        return len(self.time_series)

    def __str__(self):
        return str(self.time_series)

    def load_csv(self, csv_path):
        self.time_series = pandas.read_csv(csv_path, index_col=0, header=None,
                                           squeeze=True)

    def write_csv(self, csv_path):
        self.time_series.to_csv(csv_path, header=False)

    def load_npy_arrays(self, time_array, signal_array):
        self.time_series = pandas.Series(signal_array, index=time_array)

    def make_copy(self):
        my_copy = PandasTimeSeries()
        my_copy.time_series = self.time_series.copy()
        return my_copy

    def set_signal_from_scalar(self, scalar):
        self.time_series.fill(scalar)

    def median(self):
        return self.time_series.median()
