import nose.tools
import os.path
from ..pandas_time_series import PandasTimeSeries
from ..pandas_calculator import PandasCalculator
from ..kmeans_denoiser import KMeansDenoiser

@nose.tools.istest
def apply_kmeans_denoiser_to_time_series():
    noisy_ts = PandasTimeSeries()
    input_csv_path = os.path.join("test_data", "noisy_simple_3state.csv")
    noisy_ts.load_csv(input_csv_path)

    calculator = PandasCalculator()
    kmeans_denoiser = KMeansDenoiser(calculator)
    denoised_ts = kmeans_denoiser.run_denoising(noisy_ts, num_clust=2)

    output_csv_path = os.path.join("test_data", "output_from_kmeans_test.csv")
    denoised_ts.write_csv(output_csv_path)

@nose.tools.istest
def apply_kmeans_denoiser_to_spo_time_series():
    noisy_ts = PandasTimeSeries()
    input_csv_path = os.path.join("test_data", "spo_data.csv")
    noisy_ts.load_csv(input_csv_path)

    calculator = PandasCalculator()
    kmeans_denoiser = KMeansDenoiser(calculator)
    denoised_ts = kmeans_denoiser.run_denoising(noisy_ts, num_clust=2)

    output_csv_path = os.path.join("test_data", "spo_output_from_kmeans_test.csv")
    denoised_ts.write_csv(output_csv_path)

