#!/bin/bash

/etc/init.d/oracle-xe start

touch /empty.log
tail -f /empty.log
childPID=$!
wait $childPID
