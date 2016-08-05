# mongo2statsd
Parse the output of mongostat and send them to StatsD

## usage
``` bash
docker build -t mongo2statsd .
docker run -d mongo2statsd --mongo-host=<mongodb host> --statsd-host=<statsd host>
```

Metrics implemented:
- `mongodb.opscount.insert`
- `mongodb.opscount.update`
- `mongodb.opscount.delete`
- `mongodb.opscount.query`
- `mongodb.opscount.getmore`
- [more to come]
