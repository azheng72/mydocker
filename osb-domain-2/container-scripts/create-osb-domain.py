
import java.lang.String as jstring
import java.lang.System as jsystem
import socket

ORACLE_HOME ='/u01/oracle'
WL_HOME = ORACLE_HOME + '/wlserver'
DOMAIN_NAME = os.environ.get("DOMAIN_NAME", "base_domain")
DOMAIN_DIR = '/u01/oracle/domains/%s' % DOMAIN_NAME
APPLICATION_DIR = DOMAIN_DIR + '/applications'
MACHINENAME = os.environ.get("MACHINE_NAME", "AdminServerMachine")

oracle_db_host      = os.environ.get("DB_HOST", 'osbdb')
oracle_db_port      = os.environ.get("DB_PORT", '1521')
oracle_db_service   = os.environ.get("DB_SERVICE", 'OSB')
SOA_REPOS_DBUSER_PREFIX  = os.environ.get("SOA_REPOS_DBUSER_PREFIX",'DEV')
SOA_REPOS_DBPASSWORD     = os.environ.get("SOA_REPOS_DBPASSWORD", 'Welcome1')

# Default Managed Server created by OSB Template. Can be removed later.
MANAGED_SERVER_NAME = 'osb_server1'
MANAGED_SERVER_PORT = '8011'

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

def changeDatasourceToXA(datasource):
  print 'Change datasource '+datasource
  cd('/')
  cd('/JDBCSystemResource/'+datasource+'/JdbcResource/'+datasource+'/JDBCDriverParams/NO_NAME_0')
  set('DriverName','oracle.jdbc.xa.client.OracleXADataSource')
  set('UseXADataSourceInterface','True') 
  cd('/JDBCSystemResource/'+datasource+'/JdbcResource/'+datasource+'/JDBCDataSourceParams/NO_NAME_0')
  set('GlobalTransactionsProtocol','TwoPhaseCommit')
  cd('/')
  
  
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

def createServer(serverName, listenPort):
        print SERVERS
        if serverName not in SERVERS:
            cd('/')
            create(serverName, 'Server')
        cd('/Server/' + serverName)
        server = cmo
        server.setListenPort(listenPort)

#!-----------------------------------------
#!To track HA configuration.
#!-----------------------------------------
def setJDBCStorePrefixName():
    cd('/')
    allJDBCResources = cmo.getJDBCStores()
    for jdbcResource in allJDBCResources:
        dsname = jdbcResource.getTargets()
        if dsname!=None:
            server_name = dsname[0].getName().split()[0]
            jdbcResource.setPrefixName('REP_'+server_name+'_')

def setTLOGDataSource():
    cd('/')
    managedServers=cmo.getServers()
    for ms in managedServers:
        print ms.getName()
        if( ADMIN_SERVER_NAME!=ms.getName() and 'ics_proxy'!=ms.getName()):
            cd('/Servers/'+ms.getName())
            create(ms.getName(),'TransactionLogJDBCStore')
            cd ('TransactionLogJDBCStore/'+ms.getName())
            set('DataSource','SOALocalTxDataSource')
            set('PrefixName','TLOG_'+ms.getName()+'_')
            set('MaxRetrySecondsBeforeTLogFail',14400)
            set('MaxRetrySecondsBeforeTxException',300)
            set('RetryIntervalSeconds',30)
            cmo.setEnabled(true)

def setDeterminer():
    cd('/')
    DOMAIN_NAME=cmo.getName()
    create(DOMAIN_NAME,'JTA')
    cd('/JTA/'+DOMAIN_NAME)
    determiner=['SOADataSource_' + DOMAIN_NAME]
    set('Determiners',determiner)
    set('TimeoutSeconds',300)


#!----------------------------------------------
#! Configure Migratable targets
#!----------------------------------------------
def configMigratableTargets():
    cd('/')
    targets = cmo.getMigratableTargets()
    for target in targets:
        cd('/MigratableTargets/'+target.getName())
        set('RestartOnFailure','true')
        set('SecondsBetweenRestarts',60)
        set('NumberOfRestartAttempts',240)

#!----------------------------------------------
#! Update datasource configuration
#!----------------------------------------------


def updateDataSource(DRIVERNAME, URL, SCHEMA_POSTFIX):
    print 'drivername='+DRIVERNAME
    print 'url='+URL
    print 'schema-postfix='+SCHEMA_POSTFIX
    cd('JdbcDriverParams/NO_NAME')
    cmo.setDriverName(DRIVERNAME)
    cmo.setUrl(URL)
    cmo.setPasswordEncrypted(SOA_REPOS_DBPASSWORD)
    cd('Properties/NO_NAME')
    cd('Property/user')
    cmo.setValue(SOA_REPOS_DBUSER_PREFIX + '_' + SCHEMA_POSTFIX)


def dsExists(dsName):
  try:
    cd('/JdbcSystemResource/' + dsName + '/JdbcResource/' + dsName + '/JdbcDriverParams/NO_NAME')
    doesDsExist = true
  except Exception, err:
    doesDsExist = false

  return doesDsExist

def appendJndiName(ds, jndiName):
  cd('/JdbcSystemResource/' + ds + '/JdbcResource/' + ds + '/JDBCDataSourceParams/NO_NAME')
  jndiNames=cmo.getJNDINames()
  #jndiNames.append(jndiName)
  if jndiName: jndiNames.append(str(jndiName).strip())
  # cmo.setJNDINames(jndiNames)
  cmo.setJNDINames(array(jndiNames, java.lang.String))
  cd('/')

def printJndiNames(ds):
    cd('/JdbcSystemResource/' + ds + '/JdbcResource/' + ds + '/JDBCDataSourceParams/NO_NAME')
    jndiNames=cmo.getJNDINames()
    for s in jndiNames:
      print "jndi name in owsm: " + s
    cd('/')

#!----------------------------------------------
#! START
#!----------------------------------------------
readTemplate(WL_HOME + '/common/templates/wls/wls.jar', 'Expanded')
cmo.setName(DOMAIN_NAME)
print('Set password...')
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
set('Name', ADMIN_SERVER_NAME)
set('ListenAddress', '')
set('ListenPort', int(ADMIN_SERVER_PORT))
setOption( "AppDir", APPLICATION_DIR )
set('Machine', MACHINENAME)
SERVERS = ls('/Server', 'true', 'c')
print '======================== SERVERS============================'
print SERVERS
print '======================== SERVERS============================'
create(ADMIN_SERVER_NAME,'SSL')
cd('SSL/'+ADMIN_SERVER_NAME)
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

writeDomain(DOMAIN_DIR)
closeTemplate()

createAdminStartupPropertiesFile(DOMAIN_DIR+'/servers/'+ADMIN_SERVER_NAME+'/data/nodemanager',ADM_JAVA_ARGUMENTS)
createBootPropertiesFile(DOMAIN_DIR+'/servers/'+ADMIN_SERVER_NAME+'/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(DOMAIN_DIR+'/config/nodemanager','nm_password.properties',ADMIN_USER,ADMIN_PASSWORD)

# es = encrypt(ADMIN_PASSWORD,DOMAIN_DIR)

OSB_TEMPLATE_PATH=ORACLE_HOME+'/osb/common/templates/wls/oracle.osb_template.jar'
readDomain(DOMAIN_DIR)

cd('/')
setOption( "AppDir", APPLICATION_DIR )


cd('/')
ADMIN_SERVER_NAME = cmo.getAdminServerName()
DOMAIN_NAME = cmo.getName()

addTemplate(OSB_TEMPLATE_PATH)

#  make sure both SOA and OSB are included in the group
#osbServerGroup=["WSM-CACHE-SVR" , "WSMPM-MAN-SVR" , "JRF-MAN-SVR", "OSB-MGD-SVRS-ONLY"]
#group = getServerGroups(MANAGED_SERVER_NAME);
#setServerGroups(MANAGED_SERVER_NAME, group)

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

#!----------------------------------------------
#! Assign Default Managed Server to Cluster
#!----------------------------------------------
assign('Server',MANAGED_SERVER_NAME,'Cluster',CLUSTER_NAME)

#! #######################################################################################
#! DATA SOURCES
#! #######################################################################################
dumpStack()

print 'Change datasources'

PROPERTIES = ""
XADRIVERNAME = 'oracle.jdbc.xa.client.OracleXADataSource'
DRIVERNAME = 'oracle.jdbc.OracleDriver'
SOA_REPOS_DBURL = 'jdbc:oracle:thin:@' + oracle_db_host + ':' + str(oracle_db_port) + '/' + oracle_db_service


print 'Change datasource LocalScvTblDataSource'
cd('/JDBCSystemResource/LocalSvcTblDataSource/JdbcResource/LocalSvcTblDataSource/JDBCDriverParams/NO_NAME_0')
set('URL',SOA_REPOS_DBURL)
set('PasswordEncrypted',SOA_REPOS_DBPASSWORD)
cd('Properties/NO_NAME_0/Property/user')
set('Value',SOA_REPOS_DBUSER_PREFIX+'_STB')

#cd('/JdbcSystemResource/LocalSvcTblDataSource/JdbcResource/LocalSvcTblDataSource')
#updateDataSource(DRIVERNAME, SOA_REPOS_DBURL, 'STB')

print 'Call getDatabaseDefaults which reads the service table'
getDatabaseDefaults()  


#changeDatasourceToXA('EDNDataSource')
changeDatasourceToXA('wlsbjmsrpDataSource')
changeDatasourceToXA('OraSDPMDataSource')
changeDatasourceToXA('SOADataSource')

print 'end datasources'

setOption( "AppDir", APPLICATION_DIR )

print 'first cd=/JdbcSystemResource/mds-owsm/JdbcResource/mds-owsm'
cd('/JdbcSystemResource/mds-owsm/JdbcResource/mds-owsm')
updateDataSource(DRIVERNAME, SOA_REPOS_DBURL, 'MDS')
cd('/JdbcSystemResource/mds-owsm/JdbcResource/mds-owsm/JDBCConnectionPoolParams/NO_NAME')
cmo.setMaxCapacity(2) 
cd ('../..')

appendJndiName('mds-owsm', 'jdbc/mds/MDS_LocalTxDataSource')

cd('/JdbcSystemResource/SOADataSource/JdbcResource/SOADataSource')
updateDataSource(XADRIVERNAME, SOA_REPOS_DBURL, 'SOAINFRA')

cd('/JdbcSystemResource/SOALocalTxDataSource/JdbcResource/SOALocalTxDataSource')
updateDataSource(DRIVERNAME, SOA_REPOS_DBURL, 'SOAINFRA')

cd('/JdbcSystemResource/opss-data-source/JdbcResource/opss-data-source')
updateDataSource(DRIVERNAME, SOA_REPOS_DBURL, 'OPSS')

cd('/JdbcSystemResource/opss-audit-viewDS/JdbcResource/opss-audit-viewDS')
updateDataSource(DRIVERNAME, SOA_REPOS_DBURL, 'IAU_VIEWER')

cd('/JdbcSystemResource/opss-audit-DBDS/JdbcResource/opss-audit-DBDS')
updateDataSource(DRIVERNAME, SOA_REPOS_DBURL, 'IAU_APPEND')


setOption('BackupFiles','false')

#setJDBCStorePrefixName()
#setTLOGDataSource()
#setDeterminer()

#configMigratableTargets()

#printJndiNames('mds-owsm')


# delete OSB server
#osbServerName = 'osb_server1'
cd('/Servers')
servers = ls()
if (servers.find(MANAGED_SERVER_NAME) != -1):
   print 'Default server ' +  MANAGED_SERVER_NAME + ' exists, deleting it...'
   cd ('/')
   delete(MANAGED_SERVER_NAME, 'Server')
else:
   print 'no default osb server found !'
   pass



updateDomain()
closeDomain()
exit()

