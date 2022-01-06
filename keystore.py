#File: keystore.py
#Description: Contains functions and objects to create all accounts that will be used for the nodes

import subprocess
import json

#Function: local_account_setup
#Description: Create individual account key files to be used on the blockchain
#Parameters
#          node_count: the amount of nodes that contain accounts
# Return: a list of key files
def local_account_setup(node_count):
    i = 0
    while i < int(node_count):
        p = subprocess.Popen(['geth','account', 'new','--datadir','./tmp_data', '--password','./password.txt','--keystore','./keystore'])
        subprocess.Popen.wait(p)
        i+=1
    key_list = subprocess.check_output(['ls','./keystore'])
    return key_list.decode('UTF-8')

#Wrapper to attribute each key file name to an address
#Function: import_keyfiles
#Parameters
#          key_list: list of key files that are used to create accounts for each node
#Return: the object containing a list of key files and information pertaining to each individual file
def import_keyfiles(key_list):
    keyfiles = str(key_list).splitlines()
    files_obj= {}
    i = 0
    for file in keyfiles:
        path = "./keystore/"+ file
        d_key = "geth-dev-node_" + str(i)
        try:
            with open(path) as f:
                config_data = json.load(f)
        except OSError:
            print(f"could not open {file} file")
            exit()
        files_obj[d_key] = {
                            "address": str(config_data["address"]),
                            "file": str(file)
                           }
        i+=1
    return files_obj

#Creates the key file object to be used later when creating Dockerfiles and attributing each account to a node
#Function: create_keyfile_obj
#Parameters
#          node_count: the amount of nodes that contain accounts
#Return: the object containing all key files and the key file information
def create_keyfile_obj(node_count):
    key_list = local_account_setup(node_count)
    return import_keyfiles(key_list)