#!/bin/bash
mkdir /var/mysql_tz
mkdir /var/docker_tz
docker-compose build
sleep 60
docker-compose up -d
