#!/bin/bash
#
# Copyright (c) 2014-2015 Oracle and/or its affiliates. All rights reserved.
#
########### SIGTERM handler ############
function _term() {
 echo "Stopping container."
 echo "SIGTERM received, shutting down weblogic!" 
}

########### SIGKILL handler ############
function _kill() {
echo "SIGKILL received, shutting down weblogic!"
}

# Set SIGTERM handler
trap _term SIGTERM

# Set SIGKILL handler
trap _kill SIGKILL

#Absolute path of current file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

DOMAIN_NAME=${DOMAIN_NAME:-base_domain}
DOMAIN_HOME=/u01/oracle/domains/${DOMAIN_NAME}
MS_NAME=${MS_NAME:-ManagedServer-$(cat /etc/hostname)}
MS_LOGS=$DOMAIN_HOME/servers/${MS_NAME}/logs
ADMIN_PASSWORD=${ADMIN_PASSWORD:-welcome1}
ADMIN_HOST=${ADMIN_HOST:-wlsadmin}
ADMIN_PORT=${ADMIN_PORT:-7001}

# Create a Managed Server domain
wlst.sh -skipWLSModuleScanning $DIR/addManaged.py
mkdir -p ${MS_LOGS}

# Start Managed Server
${DOMAIN_HOME}/bin/startManagedWebLogic.sh $MS_NAME  http://${ADMIN_HOST}:${ADMIN_PORT} &> ${MS_LOGS}/${MS_NAME}.out &

touch ${MS_LOGS}/${MS_NAME}.out
tail -f ${MS_LOGS}/${MS_NAME}.out &

childPID=$!
wait $childPID
