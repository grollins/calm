import nose.tools
import os.path
from calm.pandas_time_series import PandasTimeSeries
from calm.pandas_calculator import PandasCalculator
from calm.jump_penalty_denoiser import JumpPenaltyDenoiser

@nose.tools.istest
def apply_jump_penalty_denoiser_to_time_series():
    noisy_ts = PandasTimeSeries()
    input_csv_path = os.path.join("test_data", "noisy_simple_3state.csv")
    noisy_ts.load_csv(input_csv_path)

    calculator = PandasCalculator()
    jp_denoiser = JumpPenaltyDenoiser(calculator)
    denoised_ts = jp_denoiser.run_denoising(noisy_ts, square=True, gamma=0.1,
                                            noisy=True)

    output_csv_path = os.path.join("test_data", "output_from_jp_test.csv")
    denoised_ts.write_csv(output_csv_path)