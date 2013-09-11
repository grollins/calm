from multipanel import MultipanelPlot

COLOR_SCHEME = ["#EAB086", "#EAC786", "#7995C6", "#6FC2B9", '0.65']
LINEWIDTH = 4

def plot_traces(noisy_ts, denoised_ts, clustered_ts, output_image_path):
    mp = MultipanelPlot(3, 1, figsize=(12,8))

    # ===========
    # = Panel 1 =
    # ===========
    ax = mp.get_new_ax()
    ax.plot(noisy_ts.series.index, noisy_ts.series, '-', lw=2,
            color='k')
    x_ticks = [250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    y_ticks = [-0.5, 0.0, 0.5, 1.0, 1.5]
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    x_ticklabels = ["%d" % x for x in x_ticks]
    y_ticklabels = ["%.1f" % y for y in y_ticks]
    ax.set_xticklabels(x_ticklabels)
    ax.set_yticklabels(y_ticklabels)
    for l in ax.get_xticklines():
        l.set_markersize(8) # default 4
        l.set_markeredgewidth(2.0) # default 0.5
    for l in ax.get_yticklines():
        l.set_markersize(8) # default 4
        l.set_markeredgewidth(2.0) # default 0.5
    ax.set_xlabel('Frame')
    ax.set_ylabel('Signal')
    mp.add_ax_to_plot(ax)

    # ===========
    # = Panel 2 =
    # ===========
    ax = mp.get_new_ax()
    ax.plot(denoised_ts.series.index, denoised_ts.series, '-', lw=LINEWIDTH,
            color=COLOR_SCHEME[2])
    x_ticks = [250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    y_ticks = [-0.5, 0.0, 0.5, 1.0, 1.5]
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    x_ticklabels = ["%d" % x for x in x_ticks]
    y_ticklabels = ["%.1f" % y for y in y_ticks]
    ax.set_xticklabels(x_ticklabels)
    ax.set_yticklabels(y_ticklabels)
    for l in ax.get_xticklines():
        l.set_markersize(8) # default 4
        l.set_markeredgewidth(2.0) # default 0.5
    for l in ax.get_yticklines():
        l.set_markersize(8) # default 4
        l.set_markeredgewidth(2.0) # default 0.5
    ax.set_xlabel('Frame')
    ax.set_ylabel('Signal')
    mp.add_ax_to_plot(ax)

    # ===========
    # = Panel 3 =
    # ===========
    ax = mp.get_new_ax()
    ax.plot(clustered_ts.series.index, clustered_ts.series, '-', lw=LINEWIDTH,
            color=COLOR_SCHEME[3])
    ax.set_ylim(-0.5, 1.5)
    x_ticks = [250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    y_ticks = [0.0, 1.0]
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    # x_ticklabels = [str(x) for x in x_ticks]
    x_ticklabels = ["%d" % x for x in x_ticks]
    y_ticklabels = ["dark", "bright"]
    ax.set_xticklabels(x_ticklabels)
    ax.set_yticklabels(y_ticklabels)
    for l in ax.get_xticklines():
        l.set_markersize(8) # default 4
        l.set_markeredgewidth(2.0) # default 0.5
    for l in ax.get_yticklines():
        l.set_markersize(8) # default 4
        l.set_markeredgewidth(2.0) # default 0.5
    ax.set_xlabel('Frame')
    ax.set_ylabel('Signal')
    mp.add_ax_to_plot(ax)

    mp.finalize_plot(output_image_path)
    return
