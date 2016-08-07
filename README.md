# mongo2statsd
Parse the output of mongostat and send them to StatsD

## usage
``` bash
docker build -t mongo2statsd .
docker run -d mongo2statsd --mongo-host=<mongodb host> --statsd-host=<statsd host> --metric-prefix=mongodb
```

Metrics implemented:
- `<metric-prefix>.ops_count.insert`
- `<metric-prefix>.ops_count.update`
- `<metric-prefix>.ops_count.delete`
- `<metric-prefix>.ops_count.query`
- `<metric-prefix>.ops_count.getmore`
- `<metric-prefix>.active_clients_count.read`
- `<metric-prefix>.active_clients_count.write`
- `<metric-prefix>.queued_clients_count.read`
- `<metric-prefix>.queued_clients_count.write`
- `<metric-prefix>.connection_count`
- [more to come]
