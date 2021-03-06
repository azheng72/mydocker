import os
import socket

# Initialize Variables
# ====================
# Environment Vars
hostname       = socket.gethostname()
# Admin Vars
admin_server_name = os.environ.get("ADMIN_SERVER_NAME", 'AdminServer')
admin_username = os.environ.get('ADMIN_USER', 'weblogic')
admin_password = os.environ.get('ADMIN_PASSWORD', 'welcome1')
admin_host     = os.environ.get('ADMIN_HOST', 'wlsadmin')
admin_port     = os.environ.get('ADMIN_PORT', '7001')
# Node Manager Vars
nmname         = os.environ.get('NM_NAME', 'Machine-' + hostname)
# Domain Template Vars
localTemplate  = os.environ.get('OSB_TEMPLATE', '/u01/oracle/osbManagedTemplate.jar')
domain_name = os.environ.get("DOMAIN_NAME", "base_domain")
domainPath = os.getenv('DOMAIN_HOME', '/u01/oracle/domains/' + domain_name)
# Machine Vars
machineName = os.environ.get('MACHINE_NAME', 'Machine-' + hostname)
# Managed Server Vars
managedServername = os.environ.get('MS_NAME', 'ManagedServer-' + hostname)
managedServerPort = int(os.environ.get('MS_PORT', '8011'))
# Cluster Vars
cluster_name = os.environ.get("CLUSTER_NAME", "base_cluster")

# Enter Edit Mode
# Should be Paired with saveActivate
def editMode():
    edit()
    startEdit(waitTimeInMillis=60000,
              timeOutInMillis=300000,
              exclusive="true")

def saveActivate():
    """ Save and Activate Changes
        Should be Paired with editMode
    """
    save()
    activate(block="true")

def connectToAdmin():
    """ Connect to Admin Server
    """
    connect(url='t3://' + admin_host + ':' + admin_port,
            adminServerName=admin_server_name,
            username=admin_username,
            password=admin_password)

def createMachine():
    """ Create a WebLogic Machine
        Set the machine address
    """
    cd('/')
    machine = create(machineName, 'UnixMachine')
    cd('Machines/'+machineName+'/NodeManager/'+machineName)
    cmo.setName(machineName)
    cmo.setListenAddress('')

def registerExistingServer():
    """ Register Server with Machine
        Configure Server to Listen on all network
        Associate server with a machine
    """
    cd('/')
    cd('/Servers/'+managedServername)
    registerServer(cmo)

def registerServer(srv):
    """ Register Server with Machine
        Configure Server to Listen on all network
        Associate server with a machine
    """
    srv.setListenAddress('')
    srv.setMachine(getMBean('/Machines/'+machineName))

def createServer():
    """ Create a Server
        Add it to the cluster
        Set the Listen Port
    """
    cd('/')
    srv = cmo.createServer(managedServername)    
    srv.setCluster(getMBean('/Clusters/%s' % cluster_name))
    srv.setListenPort(managedServerPort)
    return srv

def writeDomainFile():
    """ Write the domain file
        get the packed template from the Administration Server
    """
    writeTemplate(localTemplate)

def createManagedDomain():
    """ "Apply the template to create the domain
        Set the NodeManager listen address
        select and load the template that was downloaded from the Administration 
        Server.
    """
    selectCustomTemplate(localTemplate)
    loadTemplates()
    # set the Node Manager listen address and listen port.
    cd('/')
    cd('NMProperties')
    set('ListenAddress', '')

    #osbServerGroup=["OSB-MGD-SVRS-COMBINED"]
    #setServerGroups(managedServername, osbServerGroup)
    #create the domain
    writeDomain(domainPath)

def createBootPropertiesFile():
    directoryPath = domainPath+'/servers/'+managedServername+'/security'
    serverDir = File(directoryPath)
    bool = serverDir.mkdirs()
    fileNew=open(directoryPath + '/boot.properties', 'w')
    fileNew.write('username=%s\n' % admin_username)
    fileNew.write('password=%s\n' % admin_password)
    fileNew.flush()
    fileNew.close()

