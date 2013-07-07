import nose.tools
import os.path
from calm.pandas_time_series import PandasTimeSeries
from calm.pandas_calculator import PandasCalculator
from calm.jump_penalty_denoiser import JumpPenaltyDenoiser

@nose.tools.istest
def apply_jump_penalty_denoiser_with_SIC_penalty_to_time_series():
    noisy_ts = PandasTimeSeries()
    input_csv_path = os.path.join("test_data", "noisy_simple_3state.csv")
    noisy_ts.load_csv(input_csv_path)

    calculator = PandasCalculator()
    jp_denoiser = JumpPenaltyDenoiser(calculator, 'SIC')
    denoised_ts = jp_denoiser.run_denoising(noisy_ts, square=True, gamma=1.0,
                                            max_iter=5, noisy=True)

    output_csv_path = os.path.join("test_data", "output_from_SIC_jp_test.csv")
    denoised_ts.write_csv(output_csv_path)

@nose.tools.istest
def apply_jump_penalty_denoiser_with_AIC_penalty_to_time_series():
    noisy_ts = PandasTimeSeries()
    input_csv_path = os.path.join("test_data", "noisy_simple_3state.csv")
    noisy_ts.load_csv(input_csv_path)

    calculator = PandasCalculator()
    jp_denoiser = JumpPenaltyDenoiser(calculator, 'AIC')
    denoised_ts = jp_denoiser.run_denoising(noisy_ts, square=True, gamma=1.0,
                                            max_iter=5, noisy=True)

    output_csv_path = os.path.join("test_data", "output_from_AIC_jp_test.csv")
    denoised_ts.write_csv(output_csv_path)

@nose.tools.istest
def apply_jump_penalty_denoiser_with_LJ_penalty_to_time_series():
    noisy_ts = PandasTimeSeries()
    input_csv_path = os.path.join("test_data", "noisy_simple_3state.csv")
    noisy_ts.load_csv(input_csv_path)

    calculator = PandasCalculator()
    jp_denoiser = JumpPenaltyDenoiser(calculator, 'LJ')
    denoised_ts = jp_denoiser.run_denoising(noisy_ts, square=True, gamma=1.0,
                                            max_iter=5, noisy=True)

    output_csv_path = os.path.join("test_data", "output_from_LJ_jp_test.csv")
    denoised_ts.write_csv(output_csv_path)

@nose.tools.istest
@nose.tools.raises(ValueError)
def jump_penalty_denoiser_raises_exception_for_unknown_global_fcn():
    calculator = PandasCalculator()
    jp_denoiser = JumpPenaltyDenoiser(calculator, 'super_global_fcn')

