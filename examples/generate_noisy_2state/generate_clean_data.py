import sys
import re
from os import mkdir
from os.path import join, exists, basename
from subprocess import Popen, PIPE, STDOUT
from shutil import move
from glob import glob
from numpy import array, arange
from calm.pandas_time_series import PandasTimeSeries

# =============
# = Constants =
# =============
STOCHKIT_HOME="/Users/grollins/src/StochKit2.0.8"
STOCHKIT_BINARY = join(STOCHKIT_HOME, 'ssa')
MODEL_XML = "2state_model.xml"
STOCHKIT_OUTPUT_DIR = join(re.sub('\.xml$', '', MODEL_XML) + "_output",
                           "trajectories")
STOCHKIT_DIR = join("2state_model_output", "trajectories")
TRAJ_DIR = "clean_traces"

def run_stochkit(num_trajs, noisy=False):
    cmd_string = "%s -m %s -r %d -t 100 -i 2000 --keep-trajectories -f --label" % \
                 (STOCHKIT_BINARY, MODEL_XML, num_trajs)
    if noisy: print cmd_string
    process = Popen( cmd_string, shell=True, stdin=PIPE, stderr=STDOUT, stdout=PIPE)
    stdout, stderr = process.communicate()
    returncode = process.returncode

    # non-zero return code indicates something went wrong
    if returncode:
        print stdout
        print stderr
        raise RuntimeError, "Error running stochkit"

    if noisy:
        print stdout
    return

def main():
    num_trajs = int(sys.argv[1])
    run_stochkit(num_trajs, noisy=True)
    if not exists(TRAJ_DIR):
        mkdir(TRAJ_DIR)
    for path in glob( join(STOCHKIT_DIR, '*.txt') ):
        with open(path, 'r') as f:
            lines = [line.split() for line in f.readlines()]
        time_list = []
        signal_list = []
        for i, L in enumerate(lines):
            if i == 0:
                continue
            time_list.append(L[0])
            signal_list.append(L[2])
        step_num_array = arange(len(time_list))
        ts = PandasTimeSeries()
        ts.load_npy_arrays( step_num_array, array(signal_list) )
        output_path = join(TRAJ_DIR, basename(path)[:-4] + '.csv')
        ts.write_csv( output_path )
        print "Wrote", output_path

if __name__ == '__main__':
    main()