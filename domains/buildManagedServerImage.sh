#!/bin/bash
#
# MAINTAINER: Zheng Liang <zheng.liang@precise-soft.com>
#

docker build --force-rm=true --no-cache=true -t server/managed -f Dockerfile_managed_server .
