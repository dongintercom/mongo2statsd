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
        stat.process_ops_count(raw_stats)
        stat.process_active_clients_count(raw_stats)
        stat.process_queued_clients_count(raw_stats)
        stat.process_connection_count(raw_stats)

        return stat

    def process_ops_count(self, raw_stats):
        for key in ['insert', 'update', 'delete', 'query', 'getmore']:
            value = raw_stats[key]
            value = int(value if value != '*0' else 0)
            setattr(self, key, value)

    def process_active_clients_count(self, raw_stats):
        arw = raw_stats['arw']
        self.active_read_clients, self.active_write_clients = map(int, arw.split('|'))

    def process_queued_clients_count(self, raw_stats):
        qrw = raw_stats['qrw']
        self.queued_read_clients, self.queued_write_clients = map(int, qrw.split('|'))

    def process_connection_count(self, raw_stats):
        self.connection_count = int(raw_stats['conn'])


class StatSender(object):
    def __init__(self, statsd_client):
        self.statsd_client = statsd_client

    def send_stats(self, stat):
        self._send_ops_count(stat)
        self._send_active_clients_count(stat)
        self._send_queued_clients_count(stat)
        self._send_connection_count(stat)

    def _send_ops_count(self, stat):
        prefix = 'ops_count.'
        self.statsd_client.incr(prefix + 'insert', stat.insert)
        self.statsd_client.incr(prefix + 'update', stat.update)
        self.statsd_client.incr(prefix + 'delete', stat.delete)
        self.statsd_client.incr(prefix + 'query', stat.query)
        self.statsd_client.incr(prefix + 'getmore', stat.getmore)

    def _send_active_clients_count(self, stat):
        prefix = 'active_clients_count.'
        self.statsd_client.incr(prefix + 'read', stat.active_read_clients)
        self.statsd_client.incr(prefix + 'write', stat.active_write_clients)

    def _send_queued_clients_count(self, stat):
        prefix = 'queued_clients-count.'
        self.statsd_client.incr(prefix + 'read', stat.queued_read_clients)
        self.statsd_client.incr(prefix + 'write', stat.queued_write_clients)

    def _send_connection_count(self, stat):
        self.statsd_client.incr('connection_count', stat.connection_count)


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
