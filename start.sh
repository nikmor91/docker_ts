#!/bin/bash
echo mkdir /var/mysql_tz
echo mkdir /var/docker_tz
echo docker-compose build
sleep 30
echo docker-compose up -d
