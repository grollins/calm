from os import mkdir
from os.path import join, exists, basename
from glob import glob
from scipy.stats import norm
from plot_fcn import plot_clean_vs_noisy
from calm.pandas_time_series import PandasTimeSeries

MAKE_PLOTS = True
INPUT_DIR = "clean_traces"
OUTPUT_DIR = "noisy_traces"
OUTPUT_PLOT_DIR = "plots"
NOISE_LOC = 0.0
NOISE_SCALE = 0.1

def main():
    if not exists(OUTPUT_DIR):
        mkdir(OUTPUT_DIR)
    if not exists(OUTPUT_PLOT_DIR) and MAKE_PLOTS:
        mkdir(OUTPUT_PLOT_DIR)
    for path in glob( join(INPUT_DIR, '*.csv') ):
        clean_ts = PandasTimeSeries()
        clean_ts.load_csv(path)
        noise_array = norm.rvs(loc=NOISE_LOC, scale=NOISE_SCALE, size=len(clean_ts))
        noisy_ts = clean_ts.make_copy()
        noisy_ts.sum_signal_with_array(noise_array)
        output_path = join(OUTPUT_DIR, basename(path))
        noisy_ts.write_csv(output_path)
        print "Wrote", output_path
        if MAKE_PLOTS:
            output_plot_path = join(OUTPUT_PLOT_DIR, basename(path)[:-4] + '.png')
            plot_clean_vs_noisy(clean_ts, noisy_ts, output_plot_path)

if __name__ == '__main__':
    main()