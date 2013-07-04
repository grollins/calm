import nose.tools
import os.path
from calm.pandas_time_series import PandasTimeSeries
from calm.pandas_calculator import PandasCalculator
from calm.global_median_denoiser import GlobalMedianDenoiser

@nose.tools.istest
def apply_global_median_denoiser_to_time_series():
    noisy_ts = PandasTimeSeries()
    input_csv_path = os.path.join("test_data", "noisy_simple_3state.csv")
    noisy_ts.load_csv(input_csv_path)

    calculator = PandasCalculator()
    gm_denoiser = GlobalMedianDenoiser(calculator)
    denoised_ts = gm_denoiser.run_denoising(noisy_ts)
    output_csv_path = os.path.join("test_data", "output_from_gm_test.csv")
    denoised_ts.write_csv(output_csv_path)

    nose.tools.ok_(os.path.exists(output_csv_path))
    nose.tools.eq_(len(noisy_ts), len(denoised_ts))
    median_of_ts = noisy_ts.series.median()
    nose.tools.ok_((denoised_ts.series == median_of_ts).all())


