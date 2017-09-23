#!/bin/bash

export CLASSPATH=/u01/oracle/wlserver/server/lib/weblogic.jar:/u01/oracle/wlserver/modules/features/wlst.wls.classpath.jar
export CLASSPATH=$CLASSPATH:/u01/oracle/osb/lib/modules/oracle.servicebus.kernel-wls.jar
export CLASSPATH=$CLASSPATH:/u01/oracle/osb/lib/modules/oracle.servicebus.configfwk.jar
export CLASSPATH=$CLASSPATH:/u01/oracle/osb/lib/modules/oracle.servicebus.kernel-api.jar

java weblogic.WLST importOSBJarAndCustomizationFile.py
