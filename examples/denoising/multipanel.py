import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams.update({'font.size': 18})
matplotlib.rcParams.update({'axes.linewidth': 2})
matplotlib.rc('text', usetex=True)
matplotlib.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
import matplotlib.pyplot as plt

class MultipanelPlot(object):
    def __init__(self, rows, cols, figsize=(6,6)):
        self.F = plt.figure(figsize=figsize)
        self.rows = rows
        self.cols = cols
        self.current_ax_id = 1

    def get_new_ax(self):
        ax = self.F.add_subplot(self.rows, self.cols, self.current_ax_id)
        self.adjust_spines(ax)
        # ax.set_frame_on(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.tick_params(axis='both', direction='inout')
        return ax

    def add_ax_to_plot(self, ax):
        self.F.add_subplot(ax)
        self.current_ax_id += 1

    def adjust_spines(self, ax):
        for loc, spine in ax.spines.items():
            if loc in ['left','bottom']:
                pass
                # spine.set_position(('outward',10)) # outward by 10 points
            elif loc in ['right','top']:
                spine.set_color('none') # don't draw spine
            else:
                raise ValueError('unknown spine location: %s'%loc)

    def finalize_plot(self, plot_file_name):
        plt.tight_layout()
        plt.draw()
        plt.savefig(plot_file_name, bbox_inches='tight')
        plt.clf()
        print "Wrote %s" % plot_file_name
