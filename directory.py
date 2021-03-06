#File: directory.py
#Description: Contains functions and objects to create all Dockerfiles and their appropriate directories and the genesis file
import os
import subprocess
import json

#Boot node Dockerfile lines
bootnode_lines = [
    "FROM ubuntu:focal",
    "\n\n",
    "RUN apt-get update \\",
    "\n",
    "\t&& apt-get install -y wget software-properties-common \\",
    "\n",
    "\t&& rm -rf /var/lib/apt/lists/*",
    "\n\n",
    "WORKDIR \"/root\"",
    "\n\n",
    "RUN add-apt-repository -y ppa:ethereum/ethereum",
    "\n\n",
    "ARG binary",
    "\n",
    "RUN apt-get update \\",
    "\n",
    "\t&& apt-get install -y ethereum",
    "\n\n",
    "ENV nodekeyhex=\"\"",
    "\n",
    "ENV port=\"\"",
    "\n\n",
    "EXPOSE $port",
    "\n\n",
    "CMD exec bootnode -nodekeyhex $nodekeyhex",
]

#Funtion: create_node_lines
#Description: Creates the Dockerfile lines for a node containing an account
#Parameters
#          keyfile: the account number in hexadecimal format, this account will be referenced in the genesis file
#Return: lines for the individual node

def create_node_lines(keyfile):
    keyfile_copy = "COPY ./keystore/" + keyfile + " ./.ethereum/keystore/" + keyfile
    node_lines = [
        "FROM ubuntu:focal",
        "\n\n",
        "RUN apt-get update \\",
        "\n",
        "\t&& apt-get install -y wget software-properties-common \\",
        "\n",
        "\t&& rm -rf /var/lib/apt/lists/*",
        "\n\n",
        "WORKDIR \"/root\"",
        "\n\n",
        "RUN add-apt-repository -y ppa:ethereum/ethereum",
        "\n\n",
        "ARG binary",
        "\n",
        "RUN apt-get update \\",
        "\n",
        "\t&& apt-get install -y ethereum",
        "\n\n",
        "COPY password.txt ./password.txt",
        "\n\n",
        keyfile_copy,
        "\n\n",
        "COPY genesis.json ./genesis.json",
        "\n\n",
        "RUN geth init genesis.json",
        "\n\n",
        "ENV bootnodeId=\"\"",
        "\n",
        "ENV bootnodeIp=\"\"",
        "\n",
        "ENV rpcPort=\"\"",
        "\n",
        "ENV discoverPort=\"\"",
        "\n",
        "ENV bootnodePort=\"\"",
        "\n",
        "ENV networkId=\"\"",
        "\n\n",
        "EXPOSE $rpcPort",
        "\n",
        "EXPOSE $discoverPort",
        "\n\n",
        "CMD geth --bootnodes \"enode://$bootnodeId@$bootnodeIp:$bootnodePort\" --networkid $networkId "
        "--port $discoverPort --syncmode full --allow-insecure-unlock --unlock 0 --password ./password.txt --http "
        "--http.addr 0.0.0.0 --dev.period 0  --http.api \"eth,miner,personal,web3,net,debug\" --http.corsdomain \"*\" "
        "--http.port $rpcPort"
    ]
    return node_lines

#Create directories for all nodes    
#Function: create_node_directory
#Parameters
#          node_obj: the object containing information of the node to which the directory belongs to
#          keyfile_obj: object containing information about the keyfile  

def create_node_directory(node_obj,keyfile_obj):
    #generate directory name then create the directory
    dir_name = node_obj["hostname"]
    dockerfile_string = "./"+dir_name +"/Dockerfile"
    os.mkdir(dir_name)
    f  = open(dockerfile_string, "w+")
    if dir_name == "geth-bootnode":
        for line in bootnode_lines:
            f.write(line)  
    else:
        node_lines = create_node_lines(keyfile_obj["file"])
        for line in node_lines:
            f.write(str(line))

#Creates the genesis file
#Function: create_node_directory
#Parameters
#          chain_id: ID of the blockchain where work will be commited
#          keyfile_objs: contains all information of all key files

def create_genesis_file(chain_id, keyfile_objs):
    #get the time as an epoch
    #epoch = subprocess.check_output(['date', '+%s'])
    #turn epoch into hex format
    #timestamp = hex(int(epoch))
    #null = None

    genesis = {
        "config": {
            "chainId": int(chain_id),
            "homesteadBlock": 0,
            "eip150Block": 0,
            "eip150Hash": "0x0000000000000000000000000000000000000000000000000000000000000000",
            "eip155Block": 0,
            "eip158Block": 0,
            "byzantiumBlock": 0,
            "constantinopleBlock": 0,
            "petersburgBlock": 0,
            "istanbulBlock": 0,
            "ethash": {}
        },
        "nonce": "0x0",
        "timestamp": "0x00",
        "extraData": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "gasLimit": "8000000",
        "difficulty": "0x1000",
        "alloc": {},
        "number": "0x0",
        "gasUsed": "0x0"
    }
    #get the address of the key files to make sure all accounts have ether to burn
    for file in keyfile_objs.keys():
        accounts_to_allocate = genesis["alloc"]
        accounts_to_allocate["0x"+str(keyfile_objs[file]["address"])] = {"balance": "0x200000000000000000000000000000000000000000000000000000000000000"}

    with open('./genesis.json','w+') as out:
        json.dump(genesis,out,indent=2)

