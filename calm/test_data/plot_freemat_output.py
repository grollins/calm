import pandas
import pylab
from calm.pandas_time_series import PandasTimeSeries

s1 = PandasTimeSeries()
s2 = PandasTimeSeries()
s3 = PandasTimeSeries()
s1.load_csv('noisy_simple_3state.csv')
s2.load_csv('freemat_jump.csv')
s3.load_csv('output_from_jp_test.csv')
pylab.plot(s1.series.index, s1.series, 'k', lw=2)
pylab.plot(s2.series.index, s2.series, 'r', lw=2)
pylab.plot(s3.series.index, s3.series, 'b', lw=2)
pylab.show()
