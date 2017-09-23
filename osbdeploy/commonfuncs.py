
from java.io import FileInputStream
from java.io import FileOutputStream
from java.util import ArrayList
from java.util import Collections
from java.util import HashSet, HashMap
from com.bea.wli.sb.util import EnvValueTypes
from com.bea.wli.sb.util import Refs
from com.bea.wli.config.env import EnvValueQuery
from com.bea.wli.config.env import QualifiedEnvValue
from com.bea.wli.config import Ref
from com.bea.wli.config.customization import Customization
from com.bea.wli.config.customization import FindAndReplaceCustomization
from com.bea.wli.config.customization import EnvValueCustomization
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.sb.management.importexport import ALSBImportOperation

import sys
import getopt
import os
import datetime
import zipfile
import time
import glob

def createSessionName():
    sessionName = "OSBDEPLOYER_IMPORT" + str(System.currentTimeMillis())
    print( "CRETAED " + sessionName)
    return sessionName
    
    
def getALSBConfigurationMBEAN(sessionName):
    return findService(ALSBConfigurationMBean.NAME + "." + sessionName, ALSBConfigurationMBean.TYPE)
                       
                       
def getSessionManagementMBean(sessionName):
    print 'Creating session', sessionName
    try:
        #SessionMBean = findService("SessionManagement", "com.bea.wli.sb.management.configuration.SessionManagementMBean")
        SessionMBean = findService(SessionManagementMBean.NAME,SessionManagementMBean.TYPE)
        SessionMBean.createSession(sessionName)
        return SessionMBean
    except Exception, e:
        print e
        dumpStack()
        raise

def discardSession(sessionManagementMBean, sessionName):
     if sessionManagementMBean != None:
          if sessionManagementMBean.sessionExists(sessionName):
               sessionManagementMBean.discardSession(sessionName)
               print (sessionName + " - SESSION DISCARDED...")    

def readBinaryFile(fileName):
    file = open(fileName, 'rb')
    bytes = file.read()
    return bytes

