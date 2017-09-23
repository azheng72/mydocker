#!/bin/bash
#
# MAINTAINER: Zheng Liang <zheng.liang@precise-soft.com>
#

docker build --force-rm=true --no-cache=true -t soa:scripts-loaded -f Dockerfile_add_scripts_to_soa .
