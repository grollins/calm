import nose.tools
import os.path
from calm.pandas_time_series import PandasTimeSeries
from calm.pandas_calculator import PandasCalculator
from calm.threshold_denoiser import ThresholdDenoiser

@nose.tools.istest
def apply_threshold_denoiser_to_time_series():
    noisy_ts = PandasTimeSeries()
    input_csv_path = os.path.join("test_data", "noisy_simple_3state.csv")
    noisy_ts.load_csv(input_csv_path)

    calculator = PandasCalculator()
    threshold_denoiser = ThresholdDenoiser(calculator)
    denoised_ts = threshold_denoiser.run_denoising(noisy_ts, threshold_factor=3)

    output_csv_path = os.path.join("test_data", "output_from_threshold_test.csv")
    denoised_ts.write_csv(output_csv_path)
