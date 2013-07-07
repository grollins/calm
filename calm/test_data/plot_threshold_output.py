import pandas
import pylab
import matplotlib.pyplot as plt
from calm.pandas_time_series import PandasTimeSeries

s1 = PandasTimeSeries()
s2 = PandasTimeSeries()
s1.load_csv('noisy_simple_3state.csv')
s2.load_csv('output_from_threshold_test.csv')
pylab.plot(s1.series.index, s1.series, 'k', lw=1)
pylab.plot(s2.series.index, s2.series, 'r', lw=2)
# pylab.show()
pylab.clf()

s1 = PandasTimeSeries()
s2 = PandasTimeSeries()
s1.load_csv('spo_data.csv')
s2.load_csv('spo_output_from_threshold_test.csv')
pylab.plot(s1.series.index, s1.series, 'k', lw=1)
pylab.plot(s2.series.index, s2.series, 'r', lw=2)
pylab.ylim(s1.series.min(), s1.series.max()/10)
pylab.show()
pylab.clf()
