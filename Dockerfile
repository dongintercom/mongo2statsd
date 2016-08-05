FROM golang:latest
MAINTAINER ryutlis <yalewhd@gmail.com>

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install git python-dev python-pip

# install mongostat
RUN git clone https://github.com/mongodb/mongo-tools /usr/local/src/mongo-tools
WORKDIR /usr/local/src/mongo-tools
RUN mkdir bin
RUN . ./set_gopath.sh && go build -o bin/mongostat mongostat/main/mongostat.go

# prepare python prerequisite
RUN pip install statsd

# copy mongo2statsd to container
COPY . /usr/local/src/mongo2statsd

ENTRYPOINT ["/usr/local/src/mongo2statsd/docker_entrypoint.py"]
