#!/usr/bin/env python

# For option
from argparse import ArgumentParser

# Handle date and time
import time 
from datetime import datetime, timezone

# config
import yaml

# temperature logger
import tempsLogger


def get_option():

    argparser = ArgumentParser(fromfile_prefix_chars='@')
    # argparser.add_argument('filelist',help='filelist to make flat')
#    argparser.add_argument('-c', '--combine', type=int, default=1,
#                           help='combine.number')
    argparser.add_argument('-n', '--nSample', type=int, default=10,
                           help='number of sampling')
    argparser.add_argument('-c', '--cadence', type=int, default=15,
                           help='cadence of monitoring [sec]')
    argparser.add_argument('-o', '--outLog', type=str, default=None,
                           help='name of logfile')
#    argparser.add_argument('-dlc', '--drawLearningCurve', type=bool, default=False,
#                           help='Whether to draw learning curve after learning')
    return argparser.parse_args()


if __name__ == '__main__':

    args = get_option()

    # set logfile name
    if args.outLog is None:
        now_utc = datetime.now(timezone.utc)
        now_utc_str = now_utc.strftime("%Y%m%d_%H%M%S")
        logname = f"tempLog_{now_utc_str}.csv"
    else:
        logname = args.outLog

    with open('config.yaml', 'r') as file:
        config_data = yaml.safe_load(file)


    hostips=config_data['adam']['hostip']
    port=config_data['adam']['port']

    tempmon=tempsLogger.temps('logger1', hostips, port)

    fout = open(logname, 'w')

    print("UTC", file=fout, end='')
    for i, (chk, chv) in enumerate(config_data['sensor'][0].items()):
        print(f",{chk}_{chv}", file=fout, end='')
    print('', file=fout)  # change lines

    for i in range(0,args.nSample):
        # list of read temperature
        temps = tempmon.query()

        now_utc = datetime.now(timezone.utc)
        #now_utc = time.time()
        now_utc_str = now_utc.strftime("%Y-%m-%d %H:%M:%S")

        print(f"{now_utc_str}", file=fout, end='')
        for i, t in enumerate(temps):
            print(f"{t:6.2f}", file=fout, end='')
        print('', file=fout)  # change lines

        time.sleep(args.cadence)

    fout.close()