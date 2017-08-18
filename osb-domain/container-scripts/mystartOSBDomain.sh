#!/bin/bash

# Start Admin Server
DOMAIN_HOME=/u01/oracle/domains/osb_domain
ADMIN_LOGS=$DOMAIN_HOME/servers/AdminServer/logs


${DOMAIN_HOME}/startWebLogic.sh &> ${ADMIN_LOGS}/AdminServer.out &

touch ${ADMIN_LOGS}/AdminServer.out
tail -f ${ADMIN_LOGS}/AdminServer.out &

childPID=$!
wait $childPID
