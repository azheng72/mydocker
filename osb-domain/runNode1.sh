#!/bin/sh
docker run -e "MS_NAME=osb_server1" -e "MACHINE_NAME=osb1Machine" -it --network mydocker_default --name wls1 --hostname wls1 -p 8011:8011 oracle/osb_domain:12.2.1.0 /u01/oracle/container-scripts/createAndStartManagedServer.sh
