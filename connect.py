from jnpr.junos import Device
from jnpr.junos import version
import sys
from getpass import getpass
from jnpr.junos.decorators import normalizeDecorator
from jnpr.junos.utils.sw import SW
from lxml import etree
import os
os.system('clc||clear')

def connect(manual=1, method=0, hostname=0, junos_username=0, junos_password=0, port=0):#Can be used to initiate a single connection(manual=1) or multiple - manual=0; 
    
    if(manual):
        method=get_method_for_connection()#input 1)telnet 2) ssh 3) console
        credentials = get_junos_credentials()
                                            #
                                            #get credentials, format: credentials={
                                            #                                        "Hostname" : hostname,
                                            #                                        "Password" : junos_password,
                                            #                                        "Username" : junos_username,
                                            #                                        "Port" : port
                                            #                                    }
                                            #



        hostname=credentials["Hostname"]
        junos_username=credentials["Username"]
        junos_password=credentials["Password"]
        port=credentials["Port"]




    if(method==1):#Telnet
        print("Initiating Telnet session...")
        dev=Device(host=hostname, user=junos_username, passwd=junos_password, mode='telnet', port=port, use_filter=True)
    if(method==2):#SSH
        print("Initiating SSH Session...")
        dev = Device(host=hostname, user=junos_username, password=junos_password, port=port )

    #if(method==3):#Console
    

    try:
        dev.open()
        if(dev.connected):
            print("Success!")
    except Exception as err:
        print(err)
        sys.exit(1)
    #dev.close()
    
    return dev
   

def disconnect(dev):
    dev.close()
    print("Session closed")







def get_junos_credentials():
    try: #security measures
        hostname=input("Device hostname: ")
        junos_username=input("Junos OS username: ")
        junos_password=getpass("Junos OS password: ")
        while(1):
            port=int(input("Port: "))
            if(port<0 or port>65535):#checks is port is valid, raises an error if not
                raise
            break

    except:
        print("Invalid input. Exiting.")
    credentials={
        "Hostname" : hostname,
        "Username" : junos_username,
        "Password" : junos_password,
        "Port" : port
    }
    return credentials















def get_method_for_connection():#Takes user input, validates it and returns 1 for telnet, 2 for ssh, 3 for console

    
    while(1):
        print("Connection method: ")#print menu
        print("1) Telnet")
        print("2) SSH")
        print("3) Console")

        try:#validates that input is a number
            i=int(input("Choose: "))
        except:
            print("Invalid input!")
            sys.exit()



        if(i>3 or i<1):#validates if number is between 1 and 3
            print("Invalid input!")
            sys.exit()
            


        break


    #print(i)
    os.system('cls||clear')
    return i

        
if __name__ == '__main__':
    #method = get_method_for_connection()
    #credentials=get_junos_credentials()

    dev=connect()
    disconnect(dev)

