#!/bin/sh

version="0.0.2"

echo $version
docker image build -t skr8050/sre-frontend:$version .
docker push skr8050/sre-frontend:$version


