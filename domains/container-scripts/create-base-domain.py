
import java.lang.String as jstring
import java.lang.System as jsystem
import socket

ORACLE_HOME ='/u01/oracle'
WL_HOME = ORACLE_HOME + '/wlserver'
DOMAIN_NAME = os.environ.get("DOMAIN_NAME", "base_domain")
DOMAIN_DIR = '/u01/oracle/domains/%s' % DOMAIN_NAME
APPLICATION_DIR = DOMAIN_DIR + '/applications'
MACHINENAME = os.environ.get("MACHINE_NAME", "AdminServerMachine")

ADMIN_SERVER_NAME   = os.environ.get("ADMIN_SERVER_NAME", 'AdminServer')
ADMIN_USER     = 'weblogic'
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", 'welcome1')
ADMIN_SERVER_PORT = os.environ.get("ADMIN_SERVER_PORT", '7001')
JAVA_HOME      = '/usr/java/latest'
LOG_FOLDER     = '/var/log/weblogic/'
ADM_JAVA_ARGUMENTS = '-XX:PermSize=256m -XX:MaxPermSize=512m -Xms1024m -Xmx1532m -Dweblogic.Stdout='+LOG_FOLDER+'AdminServer.out -Dweblogic.Stderr='+LOG_FOLDER+'AdminServer_err.out'
OSB_JAVA_ARGUMENTS = '-XX:PermSize=256m -XX:MaxPermSize=512m -Xms1024m -Xmx1024m '

DEVELOPMENT_MODE = true

CLUSTER_NAME = os.environ.get("CLUSTER_NAME", 'base_cluster')

def createBootPropertiesFile(directoryPath,fileName, username, password):
  serverDir = File(directoryPath)
  bool = serverDir.mkdirs()
  fileNew=open(directoryPath + '/'+fileName, 'w')
  fileNew.write('username=%s\n' % username)
  fileNew.write('password=%s\n' % password)
  fileNew.flush()
  fileNew.close()


def createAdminStartupPropertiesFile(directoryPath, args):
  adminserverDir = File(directoryPath)
  bool = adminserverDir.mkdirs()
  fileNew=open(directoryPath + '/startup.properties', 'w')
  args=args.replace(':','\\:')
  args=args.replace('=','\\=')
  fileNew.write('Arguments=%s\n' % args)
  fileNew.flush()
  fileNew.close()
  
  
# ! -------------------------------------------------------
# ! SET NODEMANAGER CREDENTIALS
# ! -------------------------------------------------------

def setNodeManagerCredentials(domainHome, domainName, username, password):
    try:
        create(domainName, 'SecurityConfiguration')
        cd('/SecurityConfiguration/' + domainName)
        print '  + NodeManager Username ' + username
        set('NodeManagerUsername', username)
        set('NodeManagerPasswordEncrypted', password)
    except Exception, e:
        print e
        print 'Error while trying to NodeManager credentials!!!'
        dumpStack()
        raise




#!----------------------------------------------
#! START
#!----------------------------------------------
readTemplate(WL_HOME + '/common/templates/wls/wls.jar', 'Expanded')
cmo.setName(DOMAIN_NAME)
cd('/')
cd('Security/'+DOMAIN_NAME+'/User/weblogic')
set('Name',ADMIN_USER)
cmo.setPassword(ADMIN_PASSWORD)

if DEVELOPMENT_MODE == true:
  setOption('ServerStartMode', 'dev')
else:
  setOption('ServerStartMode', 'prod')

setOption('JavaHome', JAVA_HOME)

#!----------------------------------------------
#! Create Admin server
#!----------------------------------------------
cd('/')
create(MACHINENAME, 'UnixMachine')
cd('/Server/' + ADMIN_SERVER_NAME)
set('Name',ADMIN_SERVER_NAME )
set('ListenAddress','')
set('ListenPort'   , int(ADMIN_SERVER_PORT))
setOption( "AppDir", APPLICATION_DIR )
set('Machine', MACHINENAME)

create(ADMIN_SERVER_NAME,'SSL')
cd('SSL/' + ADMIN_SERVER_NAME)
set('Enabled', 'false')
set('ListenPort', int(ADMIN_SERVER_PORT)+1)
set('HostNameVerificationIgnored', 'True')

cd('/Machine/'+MACHINENAME)

create(MACHINENAME, 'NodeManager')
cd('NodeManager/'+MACHINENAME)
set('ListenAddress','')
set('ListenPort', 5556)
set('NodeManagerHome', DOMAIN_DIR+'/nodemanager')
setNodeManagerCredentials(DOMAIN_DIR, DOMAIN_NAME, ADMIN_USER, ADMIN_PASSWORD)

#!----------------------------------------------
#! Create Cluster
#!----------------------------------------------
cd ('/')
cluster = create(CLUSTER_NAME,'Cluster')
cd ('Cluster/' + CLUSTER_NAME)
cluster=cmo
#clusterAddress=MACHINENAME+":"+MANAGED_SERVER_PORT
#cluster.setClusterAddress(clusterAddress)
cluster.setClusterMessagingMode('unicast')
cluster.setWeblogicPluginEnabled(true)

writeDomain(DOMAIN_DIR)
closeTemplate()

createAdminStartupPropertiesFile(DOMAIN_DIR+'/servers/'+ADMIN_SERVER_NAME+'/data/nodemanager',ADM_JAVA_ARGUMENTS)
createBootPropertiesFile(DOMAIN_DIR+'/servers/'+ADMIN_SERVER_NAME+'/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(DOMAIN_DIR+'/config/nodemanager','nm_password.properties',ADMIN_USER,ADMIN_PASSWORD)


#readDomain(DOMAIN_DIR)
#updateDomain()
#closeDomain()
exit()

