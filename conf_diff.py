
from jnpr.junos import Device
from jnpr.junos import version
import sys
from getpass import getpass
import time
from jnpr.junos.decorators import normalizeDecorator
from jnpr.junos.utils.sw import SW
from jnpr.junos.utils.config import Config


hostname='192.168.100.10'
junos_username='root'
junos_password='CiscoCisco'
telnet_port='5000'

dev=Device(host=hostname, user=junos_username, passwd=junos_password, mode='telnet', port=telnet_port, use_filter=True)
print(version.VERSION)


try:
    dev.open()
    print(dev.connected)
    #print(dev.re_name)
    #print(dev.uptime)
    #print(dev.facts)
except Exception as err:
    print(err)
    sys.exit(1)


#cu = Config(dev)

conf_file='./configs/junos-config-mx.conf'
with Config(dev, mode='exclusive') as cu:
    cu.load(path=conf_file, merge=True, format='text')
    cu.commit_check()
    cu.commit()











dev.close()
print(dev.connected)