#!/usr/bin/env python

import sys
import json
import argparse
import statsd


class Stat(object):
    @classmethod
    def from_mongostat(cls, line):
        try:
            raw_stats = json.loads(line).values()[0]
        except ValueError:
            return None

        stat = cls()
        stat.process_opscount(raw_stats)

        return stat

    def process_opscount(self, raw_stats):
        for key in ['insert', 'update', 'delete', 'query', 'getmore']:
            value = raw_stats[key]
            value = int(value if value != '*0' else 0)
            setattr(self, key, value)


class StatSender(object):
    def __init__(self, statsd_client):
        self.statsd_client = statsd_client

    def send_stats(self, stat):
        self._send_opscount(stat)

    def _send_opscount(self, stat):
        prefix = 'opscount.'
        self.statsd_client.incr(prefix + 'insert', stat.insert)
        self.statsd_client.incr(prefix + 'update', stat.update)
        self.statsd_client.incr(prefix + 'delete', stat.delete)
        self.statsd_client.incr(prefix + 'query', stat.query)
        self.statsd_client.incr(prefix + 'getmore', stat.getmore)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--statsd-host", type=str, required=True)
    parser.add_argument("--statsd-port", type=int, default=8125)
    parser.add_argument("--metric-prefix", type=str, default="mongodb")
    return parser.parse_args()


def main():
    args = get_args()
    statsd_client = statsd.StatsClient(args.statsd_host,
                                       args.statsd_port,
                                       prefix=args.metric_prefix)
    stat_sender = StatSender(statsd_client)

    while True:
        line = sys.stdin.readline()
        stat = Stat.from_mongostat(line)
        if stat:
            stat_sender.send_stats(stat)


if __name__ == "__main__":
    main()
