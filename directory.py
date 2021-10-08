import os
import subprocess
import json
node_lines = [
    "FROM ubuntu:latest",
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
    "CMD geth --bootnodes \"enode://$bootnodeId@$bootnodeIp:$bootnodePort\" --networkid $networkId --datadir . --port $discoverPort --syncmode full --allow-insecure-unlock --http --http.addr 0.0.0.0  --http.api \"eth,miner,personal,web3,net,debug\" --http.corsdomain \"*\" --http.port $rpcPort"
]

bootnode_lines=[
    "FROM ubuntu:latest",
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




#create directories:
def create_node_directory(node_obj):
    #create the directory
    dir_name = node_obj["hostname"]
    dockerfile_string = "./"+dir_name +"/Dockerfile"
    os.mkdir(dir_name)
    f  = open(dockerfile_string, "w+")
    if dir_name == "geth-bootnode":
        for line in bootnode_lines:
            f.write(line)  
    else:
        for line in node_lines:
            f.write(line)

def create_genesis_file(chain_id):
    #get the time as an epoch
    epoch = subprocess.check_output(['date', '+%s'])
    #turn epoch into hex format
    timestamp = hex(int(epoch))
    null = None
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
    "timestamp": str(timestamp),
    "extraData": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "gasLimit": "0x47b760",
    "difficulty": "0x80000",
    "mixHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "coinbase": "0x0000000000000000000000000000000000000000",
    "alloc": {},
    "number": "0x0",
    "gasUsed": "0x0",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "baseFeePerGas": null
    }
    with open('./genesis.json','w+') as out:
        json.dump(genesis,out,indent=2)

