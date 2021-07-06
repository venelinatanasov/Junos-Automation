from connect import connect
from connect import disconnect
from send_configuration import send_conf


if __name__=="__main__":
    dev=connect()
    conf_file=input("File location: ")
    send_conf(dev,conf_file)
    disconnect(dev)