import cProfile
import pstats
import os.path

from calm.pandas_time_series import PandasTimeSeries
from calm.pandas_calculator import PandasCalculator
from calm.jump_penalty_denoiser import JumpPenaltyDenoiser

def main():
    noisy_ts = PandasTimeSeries()
    input_csv_path = os.path.join("..", "calm", "test_data",
                                  "noisy_simple_3state.csv")
    noisy_ts.load_csv(input_csv_path)

    calculator = PandasCalculator()
    jp_denoiser = JumpPenaltyDenoiser(calculator)
    denoised_ts = jp_denoiser.run_denoising(noisy_ts, square=True, gamma=0.1,
                                            noisy=True)
    # output_csv_path = os.path.join("test_data", "output_from_jp_test.csv")
    # denoised_ts.write_csv(output_csv_path)
    # print denoised_ts

if __name__ == '__main__':
    filename = './profile_stats.stats'
    cProfile.run('main()', filename)
    stats = pstats.Stats(filename)
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats(20)
