#!/bin/sh

version="0.0.3"

docker image build -t skr8050/sre-backend:$version .
docker push skr8050/sre-backend:$version
