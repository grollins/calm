class ThresholdDenoiser(object):
    """docstring for ThresholdDenoiser"""
    def __init__(self, calculator):
        super(ThresholdDenoiser, self).__init__()
        self.calculator = calculator

    def run_denoising(self, time_series, threshold_factor=8.):
        global_median = self.calculator.median(time_series)
        threshold = global_median * threshold_factor
        geq_inds = time_series.get_indices_where_geq(threshold)
        denoised_ts = time_series.make_copy()
        denoised_ts.set_signal_from_scalar(global_median)
        denoised_ts.set_signal_from_scalar(threshold, geq_inds)
        return denoised_ts
