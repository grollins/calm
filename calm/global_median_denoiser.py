class GlobalMedianDenoiser(object):
    """docstring for GlobalMedianDenoiser"""
    def __init__(self, calculator):
        super(GlobalMedianDenoiser, self).__init__()
        self.calculator = calculator

    def run_denoising(self, time_series):
        global_median = self.calculator.median(time_series)
        denoised_ts = time_series.make_copy()
        denoised_ts.set_signal_from_scalar(global_median)
        return denoised_ts
