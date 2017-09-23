
execfile(os.path.dirname(os.path.realpath(sys.argv[0]))+'/commonfuncs.py')

def importOSBProject(projectName,artifact):
    
    connect("weblogic", "welcome1", "t3://localhost:7001")
    domainRuntime()
    sessionName = None
    try:

        #print ("DELETE PROJECT FIRST: " + projectName)
        #print ("DELETING PROJECT :" + projectName )   
        #''' - Delete existing project '''

        #deleteProjectFromOSB(projectName)

        sessionName = createSessionName()
        SessionMBean = getSessionManagementMBean(sessionName)
	print 'SessionMBean started session'
        configurationMBean = getALSBConfigurationMBEAN(sessionName)

        print "ARTIFACT IMPORT STARTS ...."
        print ("JAR FILE: " + os.getcwd()+"/artifacts/"+artifact) 
        bytes = readBinaryFile(os.getcwd()+"/artifacts/"+artifact)
        configurationMBean.uploadJarFile(bytes)
        alsbJarInfo = configurationMBean.getImportJarInfo()
        alsbImportPlan = alsbJarInfo.getDefaultImportPlan()
        alsbImportPlan.setPassphrase(None)
        alsbImportPlan.setPreserveExistingEnvValues(false)
        refMap = HashMap()
        for r in alsbJarInfo.getResourceInfos().entrySet():
            projectRef = r.getValue().getRef()
            refMap.put(projectRef.getProjectName(), projectRef)
        print("IMPORTING JAR  " +  artifact + "..PLEASE WAIT..THIS CAN TAKE TIME..")
        result=configurationMBean.importUploaded(alsbImportPlan)
        if result.getImported().size() > 0:
            print("IMPORT SUCCESSFUL...")
        print("ACTIVATING SESSION...PLEASE WAIT..")
        try:
            SessionMBean.activateSession(sessionName, "IMPORTED BY osbDeployer PROJECT NAME: " + projectName )
            print("SESSION ACTIVATED..")
        except:
            print ("\033[92mERROR WHILE ACTIVATING IMPORT SESSION:"+ sys.exc_info()[0] +"\033[00m")
            discardSession(SessionMBean, sessionName)
            raise
            sys.exit(2)
        print("###############################################################################")
        print("\033[92mOSB ARTIFACT/JAR :   " + projectName + "  HAS BEEN IMPORTED SUCCESSFULLY....\033[00m")
        print("###############################################################################")
    
    except:
        print("\033[91mARTIFACT :   " + projectName + "  IMPORT FAILED....\033[00m")
        sys.exit(2)



def applyCustmization(customizationFile):
    SessionMBean = None
    todaysDate=datetime.datetime.now()
    try:
        domainRuntime()
        sessionName = String("Customization"+Long(System.currentTimeMillis()).toString())
        SessionMBean = findService("SessionManagement", "com.bea.wli.sb.management.configuration.SessionManagementMBean")
        SessionMBean.createSession(sessionName)
        OSBConfigurationMBean = findService(String("ALSBConfiguration.").concat(sessionName), "com.bea.wli.sb.management.configuration.ALSBConfigurationMBean")

        print( 'LOADING CUSTOMIZATION FILE ' + customizationFile)
        iStream = FileInputStream(os.getcwd() + "/artifacts/" + customizationFile)
        customizationList = Customization.fromXML(iStream)        
        OSBConfigurationMBean.customize(customizationList)
        SessionMBean.activateSession(sessionName, "CUSTMIZATION FILE: " + customizationFile+  "APPLIED BY OSB DEPLOYER ON " + str(todaysDate))
        print ('\033[92mSUCCESSFULLY COMPLETED CUSTMIZATION\033[00m')
        disconnect()
    except e:
	print e
        print("\033[91mARTIFACT :   " + customizationFile + "  IMPORT FAILED....\033[00m")
        sys.exit(2)


def deleteProjectFromOSB(projectName):
     try:
          sessionName  = "UndeployProjectStateSession_" + str(System.currentTimeMillis())         
          sessionManagementMBean = getSessionManagementMBean(sessionName)
          alsbConfigurationMBean = findService(ALSBConfigurationMBean.NAME + "." + sessionName, ALSBConfigurationMBean.TYPE)
          failed=deleteProject(alsbConfigurationMBean, projectName,sessionManagementMBean,sessionName)
          if failed=="true":
             discardSession(sessionManagementMBean, sessionName)
          else:
             print ("ACTIVATION SESSION...THIS CAN TAKE TIME.")    
             sessionManagementMBean.activateSession(sessionName, "PROJECT: " + projectName +" REMOVED BY OSB DEPLOYER")
             print ("SESSION ACTIVATED..")    
     except:
          print ("ERROR WHILST REMOVING PROJECT:"+  sys.exc_info()[0])
          discardSession(sessionManagementMBean, sessionName)
          raise


def deleteProject(alsbConfigurationMBean, projectName,sessionManagementMBean, sessionName):
     try:
          print ("TRYING TO REMOVE " + projectName)
          projectRef = Ref(Ref.PROJECT_REF, Ref.DOMAIN, projectName)                  
          if alsbConfigurationMBean.exists(projectRef):
               print ("#### REMOVING OSB PROJECT: " + projectName)
               alsbConfigurationMBean.delete(Collections.singleton(projectRef))
               print ("#### REMOVED PROJECT: " + projectName)
               failed="false"
               return failed
          else:
               
               print ("OSB PROJECT <" + projectName + "> DOES NOT EXIST")
               failed = "true"
               return failed

     except:
          print ("ERROR WHILST REMOVING PROJECT:" + sys.exc_info()[0])
          raise


try:

    jars = glob.glob('./artifacts/*.jar')
    if not jars:
        print "!!!! NO OSB JAR FOUND !!!!"
        exit(2)

    importOSBProject(jars[0].split('/')[-1][-4], jars[0].split('/')[-1])

    customfiles = glob.glob('./artifacts/*.xml')
    if not customfiles:
        print "!!!! NO OSB CUSTOMIZATION FILE FOUND !!!!"

    applyCustmization(customfiles[0].split('/')[-1])

except:
    print "Unexpected error: ", sys.exc_info()[0]
    dumpStack()
    raise




