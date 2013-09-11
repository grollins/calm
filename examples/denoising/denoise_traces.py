# standard library imports
from os import mkdir
from os.path import join, exists, basename
from glob import glob
from collections import defaultdict, Counter

# non-standard library imports
from numpy import array, float64
from pandas import DataFrame, Series

# local imports
from plot_fcn import plot_traces

# calm imports
from calm.pandas_time_series import PandasTimeSeries
from calm.pandas_calculator import PandasCalculator
from calm.jump_penalty_denoiser import JumpPenaltyDenoiser
from calm.kmeans_denoiser import KMeansDenoiser

# Constants
INPUT_CSV_DIR = "noisy_traces"
OUTPUT_CSV_DIR = "palm_traces"
OUTPUT_PLOT_DIR = "plots"
SEC_PER_FRAME = 0.05 # 50 ms
TERMINAL_DARKNESS_LENGTH = 200000 # steps


def denoise_trace(jp_denoiser, noisy_ts):
    denoised_ts = jp_denoiser.run_denoising(noisy_ts, noisy=True)
    return denoised_ts

def cluster_trace(kmeans_denoiser, denoised_ts):
    clustered_ts = kmeans_denoiser.run_denoising(denoised_ts, num_clust=2)
    return clustered_ts

def convert_trace_to_palm_format(clustered_ts):
    '''
    Expected format:
        frame_num,[0 or 1]
        frame_num,[0 or 1]
        frame_num,[0 or 1]
        frame_num,[0 or 1]
    '''
    # ==============
    # = Initialize =
    # ==============
    length_list = []
    signal_list = []
    current_signal = clustered_ts.series.ix[0]
    current_length = 0
    # ==================
    # = Get next frame =
    # ==================
    for frame_num, signal in clustered_ts.series.iteritems():
        if signal == current_signal:
            # ==========================
            # = Continue current dwell =
            # ==========================
            current_length += 1
        else:
            # ========================
            # = Dwell ended, save it =
            # ========================
            signal_list.append(current_signal)
            length_list.append(current_length)
            # ====================
            # = Start next dwell =
            # ====================
            current_signal = signal
            current_length = 1
    # ====================================
    # = No more frames, save final dwell =
    # ====================================
    signal_list.append(current_signal)
    length_list.append(current_length)
    # =====================================================================
    # = Add final dark dwell, if time series doesn't end with one already =
    # =====================================================================
    if signal_list[-1] == 0:
        pass
    else:
        signal_list.append(0) # where zero means dark
        length_list.append(1) # one frame long
    # ===================================================================
    # = If first dwell isn't dark, add initial dark dwell of one frame. =
    # ===================================================================
    if signal_list[0] == 0:
        pass
    else:
        signal_list.insert(0, 0)
        length_list.insert(0, 1)
    # =========================
    # = Convert to npy format =
    # =========================
    signal_array = array(signal_list)
    length_array = array(length_list, dtype=float64)
    # =============================
    # = Convert frames to seconds =
    # =============================
    length_array *= SEC_PER_FRAME
    # =============================
    # = Add long final dark dwell =
    # =============================
    assert signal_array[-1] == 0
    length_array[-1] = TERMINAL_DARKNESS_LENGTH
    # ==========================================================
    # = All time series should start and end with dark dwells. =
    # ==========================================================
    assert signal_array[0] == 0
    assert signal_array[-1] == 0
    # =================================
    # = Convert to time series format =
    # =================================
    palm_ts = PandasTimeSeries()
    palm_ts.series = Series(signal_array, index=length_array, dtype=object)
    palm_ts.series.replace({0:'dark', 1:'bright'}, inplace=True)
    return palm_ts

def save_ts_to_file(palm_ts, output_file_path):
    df = DataFrame({'class':palm_ts.series.values,
                    'dwell time':palm_ts.series.index.values})
    df.to_csv(output_file_path, index=False)
    print "Wrote", output_file_path

def main():
    if exists(INPUT_CSV_DIR):
        pass
    else:
        print "%s is not a valid directory" % INPUT_CSV_DIR

    if not exists(OUTPUT_CSV_DIR):
        mkdir(OUTPUT_CSV_DIR)

    if not exists(OUTPUT_PLOT_DIR):
        mkdir(OUTPUT_PLOT_DIR)

    calculator = PandasCalculator()
    jp_denoiser = JumpPenaltyDenoiser(calculator, 'AIC')
    kmeans_denoiser = KMeansDenoiser(calculator)

    input_csv_paths = glob(join(INPUT_CSV_DIR, "*.csv"))
    for p in input_csv_paths:
        print p
        noisy_ts = PandasTimeSeries()
        noisy_ts.load_csv(p)
        denoised_ts = denoise_trace(jp_denoiser, noisy_ts)
        clustered_ts = cluster_trace(kmeans_denoiser, denoised_ts)
        palm_ts = convert_trace_to_palm_format(clustered_ts)
        output_csv_path = join(OUTPUT_CSV_DIR, basename(p))
        save_ts_to_file(palm_ts, output_csv_path)
        output_plot_path = join(OUTPUT_PLOT_DIR, basename(p)[:-4] + '.png')
        plot_traces(noisy_ts, denoised_ts, clustered_ts, output_plot_path)

if __name__ == '__main__':
    main()
