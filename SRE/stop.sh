#!/bin/sh

docker-compose -f backend-docker-compose.yml stop
docker-compose -f frontend-docker-compose.yml stop