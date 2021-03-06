from read_file_dict import read_dict_file
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import UnlockError
from jnpr.junos.exception import ConfigLoadError
from jnpr.junos.exception import CommitError
from connect import connect
#host = 'dc1a.example.com'
#conf_file = 'configs/junos-config-add-op-script.conf'






def send_conf(dev, conf_file):
    

    dev.bind(cu=Config)

    # Lock the configuration, load configuration changes, and commit
    print ("Locking the configuration")
    try:
        dev.cu.lock()
    except LockError as err:
        print ("Unable to lock configuration: {0}".format(err))
        dev.close()
        return    

    print ("Loading configuration changes")
    try:
        dev.cu.load(path=conf_file, merge=True)
    except (ConfigLoadError, Exception) as err:
        print ("Unable to load configuration changes: {0}".format(err))
        print ("Unlocking the configuration")
        try:
                dev.cu.unlock()
        except UnlockError:
            print ("Unable to unlock configuration: {0}".format(err))
        dev.close()
        return

    print ("Committing the configuration")
    try:
        dev.cu.commit(comment='Loaded by example.')
    except CommitError as err:
        print ("Unable to commit configuration: {0}".format(err))
        print ("Unlocking the configuration")
        try:
            dev.cu.unlock()
        except UnlockError as err:
            print ("Unable to unlock configuration: {0}".format(err))
        dev.close()
        return

    print ("Unlocking the configuration")
    try:
        dev.cu.unlock()
    except UnlockError as err:
        print ("Unable to unlock configuration: {0}".format(err))

    # End the NETCONF session and close the connection
    dev.close()


def send_configuration_sweep(conf_file, hosts_file,count):
    for index in range(count):
        data=read_dict_file(hosts_file)
        if(data[index]['method']=='telnet'):
            method=1
        if(data[index]['method']=='ssh'):
            method=2
        hostname=data[index]['hostname']
        junos_username=data[index]['junos_username']
        junos_password=data[index]['junos_password']
        port=data[index]['port']
        print(data[index])
        
        dev=connect(manual=0, method=method, hostname=hostname, junos_username=junos_username, junos_password=junos_password, port=port)
        send_conf(dev, conf_file)

            
    


    






if __name__ == "__main__":
    count=4
    conf_file = './configs/junos-config.conf'
    hosts_file='./configs/config_device_list.conf'
    send_configuration_sweep(conf_file, hosts_file, count=4)
    