#!/bin/bash
#
# MAINTAINER: Zheng Liang <zheng.liang@precise-soft.com>
#

docker build --force-rm=true --no-cache=true -t server/admin:base -f Dockerfile_base_domain .
