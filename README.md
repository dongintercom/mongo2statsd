# mongo2statsd
Parse the output of mongostat and send them to StatsD

## usage
``` bash
docker build -t mongo2statsd .
 docker run -d mongo2statsd --mongo-host=<mongodb host> --statsd-host=<statsd host>
```
