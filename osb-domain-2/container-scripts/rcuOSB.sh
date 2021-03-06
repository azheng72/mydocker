#!/bin/bash
# 
# This script will wait until Admin Server is available.
# There is no timeout!
#
echo Run rcu for SOA Infrastucture

#Absolute path of current file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export ORACLE_HOME=/u01/oracle
export RCU_OSB_RSP=rcuResponseFile.properties
export RCU_OSB_RSP_DEL=rcuResponseFile_del.properties
export RCU_OSB_PWD=rcuOSBPasswords.txt

$ORACLE_HOME/oracle_common/bin/rcu -silent -responseFile $DIR/$RCU_OSB_RSP_DEL -f < $DIR/$RCU_OSB_PWD
$ORACLE_HOME/oracle_common/bin/rcu -silent -responseFile $DIR/$RCU_OSB_RSP -f < $DIR/$RCU_OSB_PWD
