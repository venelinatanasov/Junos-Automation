from getpass import getpass
from send_configuration import send_conf
from passlib.hash import md5_crypt
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from connect import connect
from connect import get_junos_credentials
from connect import disconnect
import sys
import os
import ast
from read_file_dict import read_dict_file

def initial_console_configuration(manual=1, conf_file='None', hosts_file=0, index=-1):#currently telnet gor gns3

    if(manual):
        dev=connect()
        cu=Config(dev)
        plaintext_pass=getpass("Set the root password for the device: ")
        pass_2=getpass("Confirm password: ")
        if(plaintext_pass != pass_2):
            print("Passwords don't match!")
            sys.exit()
        hashedpassword = md5_crypt.hash(plaintext_pass)


        set_command = 'set system root-authentication encrypted-password '  + hashedpassword


        cu.load(set_command, format='set')
        try:
            i=int(input("Commit root password? (1 or 0): "))
        except:
            sys.exit()

        if(i==1):
            cu.commit()
        else:
            print("Configuration not commited")
            sys.exit()

        try:
            i=int(input("Load additional configuration file? (1 or 0): "))
        except:
            sys.exit()
        if(i):
            conf_file=input("Filename: ")
            send_conf(dev, conf_file)
        else:
            pass




    elif(manual==0):

        if(manual==0 and hosts_file==0 and index==-1):
            print("Invalid parameters passed to function! Exiting.")
            sys.exit()



        data=read_dict_file(hosts_file)



        if(data[index]['method']=='telnet'):
            method=1
        hostname=data[index]['hostname']
        junos_username=data[index]['junos_username']
        junos_password=data[index]['junos_password']
        port=data[index]['port']
        root_password=data[index]['root_password']

        host_name=data[index]['host_name']

        dev=connect(manual=0, method=method, hostname=hostname, junos_username=junos_username, junos_password=junos_password, port=port)
        cu=Config(dev)
        
        hashedpassword = md5_crypt.hash(root_password)
        set_root_pass = 'set system root-authentication encrypted-password '  + hashedpassword
        cu.load(set_root_pass, format='set')    
        set_host_name='set system host-name ' + host_name
        cu.load(set_host_name, format='set')
        cu.commit()


        if(conf_file!='None'):
            send_conf(dev, conf_file)
        else:
            pass



    


    disconnect(dev)




def initial_console_configuration_sweep(count, conf_file, hosts_file):
    for i in range(count):
        initial_console_configuration(manual=0, conf_file=conf_file, hosts_file=hosts_file, index=i)

if __name__ == '__main__':
    initial_console_configuration_sweep(4, conf_file='./configs/initial_config.conf', hosts_file='./configs/initial_config_device_list.conf')
    #initial_console_configuration()