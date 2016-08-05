#!/usr/bin/env python

import argparse
import subprocess


MONGOSTAT_PATH = '/usr/local/src/mongo-tools/bin/mongostat'
MONGO2STATSD_PATH = '/usr/local/src/mongo2statsd/mongo2statsd.py'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mongo-host', type=str, required=True)
    parser.add_argument('--mongo-port', type=str, default='27017')
    parser.add_argument('--statsd-host', type=str, required=True)
    parser.add_argument('--statsd-port', type=str, default='8125')
    return parser.parse_args()


def main():
    args = get_args()
    mongostat_proc = subprocess.Popen(
        (MONGOSTAT_PATH,
         '-h', args.mongo_host,
         '-p', args.mongo_port,
         '--all',
         '--json'),
        stdout=subprocess.PIPE
    )
    mongo2statsd_proc = subprocess.Popen(
        (MONGO2STATSD_PATH,
         '--statsd-host', args.statsd_host,
         '--statsd-port', args.statsd_port),
        stdin=mongostat_proc.stdout,
        stdout=subprocess.PIPE
    )
    mongo2statsd_proc.communicate()

if __name__ == "__main__":
    main()
