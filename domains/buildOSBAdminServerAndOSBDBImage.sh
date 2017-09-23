#!/bin/bash
#
# MAINTAINER: Zheng Liang <zheng.liang@precise-soft.com>
#

docker network create -d bridge mydocker_default 

osbdb_exists=$(docker ps -aq --filter name=osbdb)

if [[ $osbdb_exists != '' ]]; then
    docker container rm -f osbdb
fi

docker run -dit --name osbdb --hostname osbdb --network mydocker_default osb_db

sleep 30

docker build --network mydocker_default --hostname osbadmin --force-rm=true --no-cache=true -t server/admin:osb -f Dockerfile_osb_domain .

docker commit osbdb db:osb
