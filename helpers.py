import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colorbar as cbar
import matplotlib.gridspec as gridspec
from matplotlib.dates import date2num
from matplotlib.colors import Normalize


def humansize(num, suffix='B'):
    '''human readable output of size, takes in bytes
    https://stackoverflow.com/a/1094933
    '''

    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def generate_paths(df_ps):
    grouper = df_ps.groupby('Sample_n')
    groups = grouper.groups

    def fill_tables(p):
        tid2ppid[p.PRG_TID] = p.PRG_PPID
        tid2name[p.PRG_TID] = p.PRG_name

    def get_path(p):
        parent = p.PRG_PPID
        name = p.PRG_name
        while parent:
            name = name + '—' + tid2name.get(parent, '???')
            parent = tid2ppid.get(parent)
        return name

    result = pd.Series()

    for i, k in enumerate(groups):
        if i % 10 == 0:
            print(f'\r{i/len(groups):.2f} done', end='')

        tid2ppid = {}
        tid2name = {}

        g = grouper.get_group(k)

        g.apply(fill_tables, axis=1)
        strings = g.apply(get_path, axis=1)
        result = result.append(strings)

    print()
    return result


def stripes(values, xlim=None, labels=None, vmin=0, vmax=None,
            ax=None, cax=None, title=None, cmap=None, cbar_kw=None):
    ax = ax or plt.gca()

    x1, x2 = xlim = (xlim or (0, len(values[0])-1))
    ax.set_xlim(xlim)
    if hasattr(x1, 'date'):
        x1, x2 = date2num(x1), date2num(x2)

    bar_size = .5
    hals_size = bar_size/2

    ax.set_ylim((hals_size-1, len(values)-hals_size))

    if vmax is None:
        vmax = np.max([np.max(v) for v in values])

    norm = Normalize(vmin, vmax, clip=True)
    cmap = plt.get_cmap(cmap or 'gist_heat_r')

    for i, vals in enumerate(reversed(values)):
        ax.imshow(vals[np.newaxis, :],
                  extent=(x1, x2, i-hals_size, i+hals_size),
                  cmap=cmap, norm=norm)

    ax.yaxis.set_ticks(range(0, len(values)))
    labels = reversed(labels) if labels else range(len(values), 0, -1)
    ax.set_yticklabels(labels)

    ax.set_aspect('auto')

    if not cax:
        # should've used a AxesGrid/cbar.make_axes_gridspec instead of this trickery
        cax, kw = cbar.make_axes(ax, location='top', shrink=.7, pad=.5/len(values), aspect=40)
    if title is not None:
        cax.set_title(title)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm._A = []

    cbar_kw_ = dict(orientation='horizontal')
    cbar_kw_.update(cbar_kw or {})
    ax.figure.colorbar(sm, cax=cax, **cbar_kw_)
    plt.sca(ax)
    return ax, cax


def stripes_for_tseries(values, width, freq, align_tolerance, fillna=0, **kw):
    '''A convenient wrapper around `stripes`. Creates appropriately sized figure.
       Assumes values are pandas series with tseries index. Aligns the tseries to an equal frequency.
       Plots a small comparison graph on top.
    '''
    fig = plt.figure(figsize=(width, len(values)))

    # configure the layout
    gs = gridspec.GridSpec(3, 1, height_ratios=(1, 1.3, len(values)), hspace=4)
    cb_ax = fig.add_subplot(gs[0])
    gs = gridspec.GridSpec(3, 1, height_ratios=(1, 1.3, len(values)), hspace=0)
    main_ax = fig.add_subplot(gs[2])
    extra_ax = fig.add_subplot(gs[1], sharex=main_ax)

    # align values
    # our tseries indexed values could have gaps, different length and frequency
    # so we align them to a uniform index, and fill gaps in the data to `fillna`
    values_ = []
    xmin = min(ts.index[0] for ts in values)
    xmax = max(ts.index[-1] for ts in values)
    uniform_index = pd.date_range(xmin, xmax, freq=freq)
    ref_df = pd.DataFrame(index=uniform_index)
    for tseries in values:
        # maybe I should've used resampler here instead
        df = pd.merge_asof(ref_df, pd.DataFrame(tseries), left_index=True, right_index=True,
                           tolerance=pd.Timedelta(align_tolerance), direction='nearest')
        values_.append(df.iloc[:,0].fillna(fillna))
    values = values_

    # stripes plot
    stripes(values, ax=main_ax, cax=cb_ax, xlim=(xmin, xmax), **kw)
    plt.setp(main_ax.yaxis.get_ticklabels(), size=9)
    plt.setp(cb_ax.xaxis.get_ticklabels(), size=8)

    # adjust extra axes
    extra_ax.yaxis.set_tick_params(bottom='off', labelbottom='off', which='both')
    extra_ax.xaxis.set_tick_params(bottom='off', labelbottom='off', which='both')

    return fig, (main_ax, cb_ax, extra_ax)
