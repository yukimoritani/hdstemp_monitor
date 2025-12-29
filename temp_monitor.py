#!/usr/bin/env python

# For option
from argparse import ArgumentParser

# Handle date and time
import time 
from datetime import datetime, timezone

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
    argparser.add_argument('-o', '--outLog', type=str, default='temps.log',
                           help='name of logfile')
#    argparser.add_argument('-dlc', '--drawLearningCurve', type=bool, default=False,
#                           help='Whether to draw learning curve after learning')
    return argparser.parse_args()


if __name__ == '__main__':

    args = get_option()

    hostip=['10.0.0.1']
    port=502

    tempmon=tempsLogger.temps('logger1', hostip, port)

    fout = open(args.outLog, 'w')

    for i in range(0,args.nSample):
        # list of read temperature
        temps = tempmon.query()

        now_utc = datetime.now(timezone.utc)
        #now_utc = time.time()
        now_utc_str = now_utc.strftime("%Y-%m-%d %H:%M:%S")

        print(f"{now_utc_str},{temps[0]:6.2f},{temps[0]:6.2f},{temps[2]:6.2f},{temps[3]:6.2f},{temps[4]:6.2f},{temps[5]:6.2f},{temps[6]:6.2f}", file=fout)

        time.sleep(args.cadence)

    fout.close()