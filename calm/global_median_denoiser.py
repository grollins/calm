from calm.pandas_calculator import PandasCalculator

class GlobalMedianDenoiser(object):
    """docstring for GlobalMedianDenoiser"""
    def __init__(self):
        super(GlobalMedianDenoiser, self).__init__()
        self.calculator = PandasCalculator()

    def run_denoising(self, time_series):
        global_median = self.calculator.median(time_series)
        denoised_ts = time_series.make_copy()
        denoised_ts.set_signal_from_scalar(global_median)
        return denoised_ts
