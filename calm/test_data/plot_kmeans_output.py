import pandas
import pylab
import matplotlib.pyplot as plt
from calm.pandas_time_series import PandasTimeSeries

s1 = PandasTimeSeries()
s2 = PandasTimeSeries()
s1.load_csv('noisy_simple_3state.csv')
s2.load_csv('output_from_kmeans_test.csv')
clust0_inds = s2.get_indices_where_lt(1.0)
clust1_inds = s2.get_indices_where_geq(1.0)
pylab.plot(s1.series.index, s1.series, 'k', lw=2)
pylab.plot(s1.series.index[clust0_inds], s1.series[clust0_inds], 'bo', ms=5)
pylab.plot(s1.series.index[clust1_inds], s1.series[clust1_inds], 'ro', ms=5)
pylab.show()
pylab.clf()
pylab.plot(s2.series.index, s2.series, 'k', lw=2)
pylab.plot(s2.series.index[clust0_inds], s2.series[clust0_inds], 'bo', ms=5)
pylab.plot(s2.series.index[clust1_inds], s2.series[clust1_inds], 'ro', ms=5)
pylab.ylim(-0.2, 1.2)
pylab.show()
pylab.clf()

s1 = PandasTimeSeries()
s2 = PandasTimeSeries()
s1.load_csv('spo_data.csv')
s2.load_csv('spo_output_from_kmeans_test.csv')
clust0_inds = s2.get_indices_where_lt(1.0)
clust1_inds = s2.get_indices_where_geq(1.0)
pylab.plot(s1.series.index[clust0_inds], s1.series[clust0_inds], 'ko', ms=3)
pylab.plot(s1.series.index[clust1_inds], s1.series[clust1_inds], 'ro', ms=3)
pylab.show()
pylab.clf()
pylab.plot(s2.series.index[clust0_inds], s2.series[clust0_inds], 'ko', ms=3)
pylab.plot(s2.series.index[clust1_inds], s2.series[clust1_inds], 'ro', ms=3)
pylab.ylim(-0.2, 1.2)
pylab.show()
pylab.clf()