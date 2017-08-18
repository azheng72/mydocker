#!/bin/sh
docker run -it --name osbadmin --network mynet --hostname osbadmin -p 8011:8011 -p 7001:7001 oracle/osb_domain:12.2.1.0
