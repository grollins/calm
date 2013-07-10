from numpy import atleast_2d
from sklearn.cluster import KMeans

class KMeansDenoiser(object):
    """docstring for KMeansDenoiser"""
    def __init__(self, calculator):
        super(KMeansDenoiser, self).__init__()
        self.calculator = calculator

    def run_denoising(self, time_series, num_clust=2, noisy=False):
        clusterer = KMeans(init='k-means++', n_clusters=num_clust, n_init=10)
        ts_2d = atleast_2d(time_series.series).T
        clusterer.fit( ts_2d )
        print clusterer.labels_
        denoised_ts = time_series.make_copy()
        denoised_ts.set_signal_values_from_npy_array( clusterer.labels_ )
        return denoised_ts

