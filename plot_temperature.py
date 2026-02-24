#!/home/moritani/anaconda3/envs/analysis/bin/ python

from locale import normalize
import numpy as np
import pandas as pd
# from scipy import ndimage
# from scipy.optimize import curve_fit
import scipy.signal as signal

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# import matplotlib.patches as patches

# For option
from argparse import ArgumentParser

# Handle date and time
from datetime import datetime

# logging
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO)


def get_option():

    argparser = ArgumentParser(fromfile_prefix_chars='@')
    argparser.add_argument('file', help='file of time and observable')
    #argparser.add_argument('tscp', help='tsc log for dome position')
    #argparser.add_argument('tscr', help='tsc log for dome speed')
    #argparser.add_argument('fmax', type=float, help='minimum angular frequency range')
    #argparser.add_argument('fmin', type=float, help='maximum angular frequency range')
    #argparser.add_argument('-n', '--nfreq', type=int, default=100,
    #                       help='number of freq. point to look into')
    #argparser.add_argument('-f', '--fileList', nargs='*', type=str, default='',
    #                       help='additional file list')
    # argparser.add_argument('-fr', '--reffarfield', type=str, default='',
    #                        help='far field reference image file')
    # argparser.add_argument('-c', '--combine', type=int, default=1,
    #                        help='combine.number')
    argparser.add_argument('-s', '--start', type=str, default='2025-12-31 00:00:00',
                           help='Start time for plot. Format is yyyy-mm-dd HH:MM:SS')
    argparser.add_argument('-e', '--end', type=str, default='2026-01-01 00:00:00',
                           help='End time for plot. Format is yyyy-mm-dd HH:MM:SS')
    argparser.add_argument('-sf', '--suffix', type=str, default='',
                           help='suffix of figures name')
#    argparser.add_argument('-dlc', '--drawLearningCurve', type=bool, default=False,
#                           help='Whether to draw learning curve after learning')
    return argparser.parse_args()

def change_timeformat(df):

    if 'ms' in df['time']:
        ms = int(df['time'][18:].replace('ms ',''))
        df['time'] = df['time'][:17] + f'.{ms:03d} '
        print(f'{df["time"]}\r', end='')
    else:
        df['time'] = df['time'][:-1] + '.0' + df['time'][-1:]
        print(f'{df["time"]}\r', end='')
    return df


def read_data(fname):

    df = pd.read_csv(fname,
                     delimiter=',', skipinitialspace=True,
                     )
    df['time_hst'] = pd.to_datetime(df['UTC'], format='%Y-%m-%d %H:%M:%S')
    df['time_hst'] = df['time_hst'] + pd.Timedelta(hours=-10)
    logging.debug(df['time_hst'][:3])

    return df


def read_tsc(inname):

    df = pd.read_csv(inname)
    df = df.rename(columns={'# datetime':'time'})
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S.%f')

    return df


def plot_time(fname, tstart, tend, subMean=False, fname_suf=''):

    # read the data
    df = read_data(fname)

    fig='test'
    fig, axs = plt.subplots(num=fig, nrows=1, ncols=1, sharex=True, sharey=False,
                        layout='constrained', figsize=(10,6))

    # temperature
    axs.minorticks_on()
    axs.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    tmin = datetime.strptime(tstart, '%Y-%m-%d %H:%M:%S')
    tmax = datetime.strptime(tend, '%Y-%m-%d %H:%M:%S')
    axs.set_xlim(xmin=tmin, xmax=tmax)

    # ax.set_title("Result of Lomb-Scargle analysis")
    axs.set_xlabel("time (HST)")
    if subMean:
        axs.set_ylabel("value -mean(value) [C]", fontsize=8)
    else:
        axs.set_ylabel("value [C]", fontsize=8)

    for i, tname in enumerate(df.columns[1:-1]):
        # mean
        if subMean:
            meanx=np.nanmean(df.iloc[:,i+1])
            labelx=f"{tname} (mean={meanx:.2f})"
        else:
            meanx=0.
            labelx=f"{tname}"
        axs.plot(df['time_hst'], df.iloc[:,i+1]-meanx, alpha=0.5, 
            marker='+', linestyle='-', ms=0., lw=0.5, label=labelx)
    axs.legend(fontsize=8)
    axs.set_ylim(ymin=22., ymax=27.)
    axs.grid(which='both', linestyle='--', alpha=0.4)

    #now = datetime.now()
    savefile = f"plot_vib_time_{fname_suf}.png"
    plt.savefig(savefile, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':

    args = get_option()

    plot_time(args.file, args.start, args.end, subMean=False, fname_suf=args.suffix)
