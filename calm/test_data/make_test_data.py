import numpy
from calm.pandas_time_series import PandasTimeSeries

def make_three_state_data():
    signals = [(300, 0.0),
               (200, 1.0),
               (50,  0.0),
               (100, 1.0),
               (50,  2.0),
               (100, 1.0),
               (100, 0.0),
               (100, 1.0),
               (100, 0.0)]
    signal_array_list = []
    for s in signals:
        length, mean_value = s
        s_array = numpy.ones([length]) * mean_value
        signal_array_list.append(s_array)
    y = numpy.concatenate(signal_array_list)
    x = numpy.arange(len(y))
    smooth_ts = PandasTimeSeries()
    smooth_ts.load_npy_arrays(x, y)
    smooth_ts.write_csv("smooth_simple_3state.csv")

    noise = 0.25
    signal_array_list = []
    for s in signals:
        length, mean_value = s
        s_array = numpy.ones([length]) * mean_value +\
                  numpy.random.normal(loc=0.0, scale=noise, size=length)
        signal_array_list.append(s_array)
    y = numpy.concatenate(signal_array_list)
    x = numpy.arange(len(y))
    noisy_ts = PandasTimeSeries()
    noisy_ts.load_npy_arrays(x, y)
    noisy_ts.write_csv("noisy_simple_3state.csv")

def main():
    make_three_state_data()

if __name__ == '__main__':
    main()