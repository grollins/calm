class ThresholdDenoiser(object):
    """docstring for ThresholdDenoiser"""
    def __init__(self, calculator):
        super(ThresholdDenoiser, self).__init__()
        self.calculator = calculator

    def run_denoising(self, time_series, threshold_factor=8., noisy=False):
        global_median = self.calculator.median(time_series)
        threshold = abs(global_median * threshold_factor)
        if noisy:
            print "median:", global_median
            print "threshold:", threshold
        denoised_ts = time_series.make_copy()
        self.calculator.subtract_scalar(denoised_ts, global_median)
        geq_inds = denoised_ts.get_indices_where_geq(threshold)
        denoised_ts.set_signal_from_scalar(0.)
        denoised_ts.set_signal_from_scalar(threshold, geq_inds)
        return denoised_ts
