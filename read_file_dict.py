import ast
import sys


def read_dict_file(hosts_file):
    try:
        f=open(hosts_file,'r')
        data=f.read()
        f.close()

        data=data.split()
        data="".join(data)
        data=ast.literal_eval(data)
        return data
    except:
        print("File read error! Exiting.")
        sys.exit()
