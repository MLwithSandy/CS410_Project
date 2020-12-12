#!/bin/sh

version="0.0.4"

docker image build -t skr8050/sre-backend:$version .
docker push skr8050/sre-backend:$version
