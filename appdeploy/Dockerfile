# LICENSE CDDL 1.0 + GPL 2.0
#
# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# 
# ORACLE DOCKERFILES PROJECT
# --------------------------
# This Dockerfile extends the Oracle WebLogic image built under 1221-domain with tag name '1221-domain'
#
# It will deploy any package defined in APP_PKG_FILE located in APP_PKG_LOCATION
# into the DOMAIN_HOME with name defined in APP_NAME
#
# HOW TO BUILD THIS IMAGE
# -----------------------
# Run: 
#      $ docker build -t 1221-appdeploy .
#

# Pull base image
# ---------------
FROM ws_domain 

# Maintainer
# ----------
MAINTAINER Bruno Borges <bruno.borges@oracle.com>

# Define variables
ENV APP_NAME="NfsdxWSv2" \
    APP_PKG_FILE="NfsdxWS-2.0-SNAPSHOT.ear" \
    APP_PKG_LOCATION="/u01/oracle"

# Copy files and deploy application in WLST Offline mode
COPY container-scripts/* /u01/oracle/

RUN wlst.sh /u01/oracle/app-deploy.py
