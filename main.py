#https://docs.docker.com/engine/install/linux-postinstall/

import json
import pyaml
import subprocess
import compose
import directory
import keystore

#main loop
if __name__ == "__main__":
    arguments = compose.ingest_config_file()
    config_file = arguments.config_file
    #open json file
    try:
        with open(config_file) as config_f:
            config_data = json.load(config_f)
    except OSError:
        print(f"could not open {config_file} file")
        exit()
    
    #grab all variables
    bnode_keyfile = config_data["key"]
    chain = config_data["chain_id"]
    bnodeIP = config_data["bootnode_ip"]
    bnodePort = config_data["bootnode_port"]
    networkRange = config_data["ip_range"]
    node_count = config_data["node_count"]

    #open bootkey file 
    try:
        f = open(bnode_keyfile, "r")
    except OSError:
        print(f"could not open {bnode_keyfile} file")
        exit()

    #key was read in correctly
    hexkey = f.read()

    #transform that key into a enode string
    enodekey = subprocess.check_output(['bootnode','-nodekeyhex',hexkey, '-writeaddress'])
    enodekey = enodekey.decode("utf-8")
    enodekey = enodekey.rstrip('\n')

    # create all accounts
    keyfile_objs = keystore.create_keyfile_obj(node_count)
    #need to create accounts from keys, save
    #create the genesis file
    directory.create_genesis_file(chain,keyfile_objs)
    
    #start the compose file
    initial = {
                "version": "\"3\"",
                'services': {}
              }

    #create the bootnode data
    bnode_data = compose.create_bootnode_data(hexkey,enodekey,bnodeIP,bnodePort)
    #create the bootnode portion of the compose file
    bnode = compose.create_bootnode(bnode_data)
    directory.create_node_directory(bnode,None)
    initial["services"][bnode["hostname"]] = bnode

    #do it for other nodes
    nodes = compose.create_nodes_wrapper(networkRange, node_count, bnode_data,chain)
    for name in nodes.keys():
        initial["services"][name] = nodes[name]
        directory.create_node_directory(nodes[name],keyfile_objs[name])
    initial["networks"] = compose.create_network(networkRange)
    initial["volumes"] = compose.create_volumes(node_count)
    
    text = pyaml.dump(initial,sort_keys=False)
    text.encode("UTF-8")
    with open('docker-compose.yaml','w',encoding="utf-8") as file:
        file.write(text)

    
     
    

