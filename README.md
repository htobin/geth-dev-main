# Documentation

# Purpose
To create a simulated network of Ethereum nodes that can store Ether, mine Ether, and deploy smart contracts. This simulation uses *Docker* to create an instance(container) of each node. In it's current iteration, users can use the host machine's terminal in Linux and MacOS to access nodes and control functionality. Each container is running the Ethereum client *Geth*. This client is what initializes the nodes and keeps them running on the network. Nodes can be communicated to with the use of the *Web3.py* library. Web3.py allows users to interact directly with the nodes via their geth interface. Actions such as: start mining, checking mining status, check the ether balance, and creating new accounts can all be done through the host machine's terminal. Once there are a few nodes mining, users can then use *Brownie* framework to compile and deploy smart contracts onto the simulated network.

# Dependencies on Linux
- ### [Python](https://www.python.org/downloads/): version 3.8.10 or greater
- ### [pip](https://pip.pypa.io/en/stable/cli/pip_download/): version 20.0.2 
- ### [Web3.py](https://web3py.readthedocs.io/en/stable/): version 5.24.0 or greater
- ### [Docker](https://docs.docker.com/get-docker/): Docker version 20.10.7, build 20.10.7-0 ubuntu5~20.04.2
    - ### [Docker Compose v2](https://docs.docker.com/compose/cli-command/)
- ### [Geth](https://geth.ethereum.org/docs/install-and-build/installing-geth): Version: 1.10.14-stable
- ### [Brownie](https://eth-brownie.readthedocs.io/en/stable/): Brownie v1.17.0




# Directories and files for blockchain configuration, initialization, and node interaction
- ## main.py
    - Uses the config.json configuration file to generate the Docker Compose file, key files for each account, 
- ## compose.py
    - Contains function to create different sections of the Docker Compose file. The Docker Compose file is used for container composition.  
- ## directory.py
    - Contains function to create Dockerfiles for each node which is represented as a Docker container. Each container is currently an instance of Linux. Dockerfiles allow the container to run automatically, meaning that software can be installed, files can be copied into the instance, ports can be opened, and running commands in the container's terminal.
    - Also creates the genesis file, which is used to establish certain conditions for the Ethereum network and the nodes connected to it at startup.
- ## keystore.py
    - Contains functions to import the key files. Keyfiles are used for wallets nodes that allow Geth to recognize which funds belong to which nodes. 
- ## nodes.py
    - Contains functions that use the Web3.py library to interact with nodes. 
    - Current functions:
        - Create dummy accounts, with 0 ether(planning to remove)
        - have all but the first node mine for ethereum to produce blocks for the blockchain
        - stop nodes that are currently mining
        - unlock all nodes for fund usage
        - check if nodes are mining
        - check balance of all nodes
        - identify a node to use, and look for a particular transaction on the blockchain
- ## /geth-dev-node_#
    - Contains the Dockerfile to create the container and image of each node
- ## /keystore
    - Contains the keyfiles for each wallet node, contains information that allow dev nodes to commit transactions and deploy smart contracts
    - keystore files are created when main.py is ran
- ## cleanup (Directory)
    - cleandocker.sh: Removes: containers, images, volumes, and networks from Docker
    - cleanfiles.sh Removes: node directories, genesis file, Docker Compose file, and node keyfiles
- ## clean.sh
    - Cleans all Docker artifacts and additional directories.

# Configuration file: config.json
    {
        "key":"./bootnode.key",
            - location of the boot node key
        "bootnode_ip": "172.16.0.101",
            - the ip of the boot node
        "bootnode_port":"30301",
            - the discovery port on the boot node that is used to recieve messages from other nodes 
        "ip_range": "172.16.0.0/24",
            - IP range for all nodes
        "node_count": "3",
            - determines how many additional wallet nodes will be added
        "chain_id": "666666"
            - customizes the chain ID, in case developers want to make different chains with conditions
    }

# Genesis file structure: genesis.json
This is the genesis file which is used by the boot node and gives all of the conditions that are given at the start of the network. For example it can indicate which block to start at along with 

    "config": {
        "chainId": 666666,
            - the ID of the blockchain is used by other nodes to identify which blockchain they are using to perform work

        *All fields below are used to indicate which block is the first block, the details of the different types of blocks are beyond the scope of this project*

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
    "timestamp": "0x61ca9f5b",
        - generated in the directory.py code. This is the epoch in which block 0 is generated, block 0 isn't mined because there are no transactions. This is known as a the genesis block.
    "extraData": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "gasLimit": "0x47b760",
        - makes sure that accounts don't spend too much gas for a single transaction
      "difficulty": "0x00001",
        - The lower this number is the less processing power is needed to mine blocks
      "mixHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "coinbase": "0x0000000000000000000000000000000000000000",
      "alloc": {
        - all accounts in the "alloc" field are generated with a set amount of ethe.
        "0xdb3e57f6a5b8261240957fb1dc1fa2881614c7cc": {
          "balance": "0x200000000000000000000000000000000000000000000000000000000000000"
        },
        "0x2732455d19d965a6f806f004fac86167e950f7ba": {
          "balance": "0x200000000000000000000000000000000000000000000000000000000000000"
        },
        "0xcbf2c4cc3b471230d1901f4c93f97f7d001396d7": {
          "balance": "0x200000000000000000000000000000000000000000000000000000000000000"
        }
      },
      "number": "0x0",
      "gasUsed": "0x0",
      "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "baseFeePerGas": null

# Docker Compose file structures: docker-compose.yaml
These are segments within the Docker Compose file that are generated from the compose.py set of functions. I've added comments below each field or variable to explain their purpose in the compose file
## bootnode structure in Compose file
    geth-bootnode:
        hostname: geth-bootnode 
        environment:
            - nodekeyhex=533faaa4fadeb29d47ccaa68d7c0039e42ecd2df72641b276e1b207380866dda
                - this is the public key for the boot node, it allows other nodes to connect to the boot node.
            - port=30301
                - this is the port of the boot node container, where nodes on the network will use to access 
                  it, this variable is referenced in the Dockerfile
        build:
            context: ./geth-bootnode
                - the working directory where any files used by the container can be found
        ports:
            - 30301:30301/udp
                - formatted for [host port:container point], designates a host port that the container will use
        volumes:
            - bootnode:/root/.ethash
                - [source voulme: destination voulme], can also be a local source such as directory if    looking for maximum sync potential 
        networks:
            chainnet:
                - name of the network that connects all of the nodes
                ipv4_address: 172.16.0.101
                    - IP address of the boot node

## Wallet node structire in Compose file
    geth-dev-node_0:
        hostname: geth-dev-node_0
        depends_on:
            - tells Docker that this container needs to wait for another containter to be build first
            - geth-bootnode
        environment:
            -bootnodeId=c606d12450ec5cdbe03806b85f8e4988df9e56c0209e6078c03b3ab0f84e5055da506358cb42342196a05e40396bb556cf599fc410561d96c99ab8f45e08861d
                - public hex ID that allows this node to connect to the boot node
            - bootnodeIp=172.16.0.101
                - IP of the boot node
            - rpcPort=8545
                - port on the container that allows outside clients to access the nodes
            - discoverPort=30302
                - port used to connect to the boot node, this makes the node discoverable by other clients
            - bootnodePort=30301
                - port on the boot node 
            - networkId=666666
                - ID of the Ethereum network that this node will connect to
        build:
            context: . 
            - the working directory where any files used by the container can be found
        dockerfile: ./geth-dev-node_0/Dockerfile
            - location of the Dockerfile
        container_name: geth-dev-node_0
            - Name for the container
        healthcheck:
            - checks to see if the container is using that port.
            test: 'wget http://localhost:8545'
            interval: 2s
            timeout: 5s
            retries: 30
        volumes:
            - eth-data-0:/root/.ethhash
            - [source voulme: destination voulme], can also be a local source such as directory if    looking for maximum sync potential 
        ports:
            - 8545:8545
                - formatted for [host port:container point], designates a host port that the contain will use
            - 30302:30302/udp
                - formatted for [host port:container point], designates a host port that the contain will use
        networks:
            chainnet:
                ipv4_address: 172.16.0.2


# Dockerfile format

## Boot node Dockerfile structure
    FROM ubuntu:latest
        - Docker has images of containers that you can use as a base for your container

    RUN apt-get update \
        && apt-get install -y wget software-properties-common \
        && rm -rf /var/lib/apt/lists/*
            - Get software to download and use Ethereum and Ethereum client software

    WORKDIR "/root"
        - set the working directory to root

    RUN add-apt-repository -y ppa:ethereum/ethereum

    ARG binary
    RUN apt-get update \
        && apt-get install -y ethereum
            - Install Ethereum and Ethereum client software

    ENV nodekeyhex=""
    ENV port=""
        - All enviornmental varaibles are loaded from the docker-compose.yaml file and used below
    EXPOSE $port

    CMD exec bootnode -nodekeyhex $nodekeyhex
        - starts the boot node in this container, using the bootnode key file
    
## Wallet node Dockerfile structure                
    FROM ubuntu:latest
        - Docker has images of containers that you can use as a base that you can use for your container

    RUN apt-get update \
        && apt-get install -y wget software-properties-common \
        && rm -rf /var/lib/apt/lists/*
            - Get software to download and use Ethereum and Ethereum client software

    WORKDIR "/root"
        - set the working directory to root

    RUN add-apt-repository -y ppa:ethereum/ethereum
        - Get Ethereum and Ethereum client software

    ARG binary

    RUN apt-get update \
        && apt-get install -y ethereum
            - Install Ethereum and Ethereum client software

    COPY password.txt ./password.txt
        - Copy the password file that will be used to initiate the wallet node

    COPY ./keystore/UTC--2021-12-29T01-46-08.660237000Z--b37f2566c04bdfb86ad1740d1ab67f49207f06bc 
        - The source key file to copy over
    ./.ethereum/keystore/UTC--2021-12-29T01-46-08.660237000Z--b37f2566c04bdfb86ad1740d1ab67f49207f06bc
        - key file destination in the container 

    COPY genesis.json ./genesis.json
        - copy the genesis file information 

    RUN geth init genesis.json
        - initialize the genesis information, so this node is in sync with other nodes on the network

    ENV bootnodeId=""
    ENV bootnodeIp=""
    ENV rpcPort=""
    ENV discoverPort=""
    ENV bootnodePort=""
    ENV networkId=""
        - All enviornmental varaibles are loaded from the docker-compose.yaml file and used below

    EXPOSE $rpcPort
    EXPOSE $discoverPort

    *geth command line breakdown*
    CMD geth 
    --bootnodes "enode://$bootnodeId@$bootnodeIp:$bootnodePort" 
        - identifiies the bootnode on the network
    --networkid $networkId 
        - identifies the blockchain that the node is connecting to
    --port $discoverPort 
        - identifies the discover port used to communicate with the boott node
    --syncmode full 
        - determines how much data that the container needs to store in order to properly sync with the blockchain
    --allow-insecure-unlock 
        - allows for remote access to the wallet
    --unlock 0 
        - unlocks the first account that is in the wallet
    --password ./password.txt 
        - identifies the location of the password text file
    --http 
        - uses HTTP for network protocol
    --http.addr 0.0.0.0 
        - server listening interface: set to 0
    --http.api "eth,miner,personal,web3,net,debug" 
        - libraries available to use with the wallet node, used to interact with web3.py library
    --http.corsdomain "*" 
        - HTTP path prefix: not sure what this means
    --http.port $rpcPort
        - RPC port that will be used to communicate with web3.py library

# Contract deployment using Brownie framework: /token
- ## /token/contracts
    - Default solidity contracts
- ## /token/scripts
    - python script to deploy the contract
- ## /token/tests
    - test your contracts on your network.

# Running the program
In it's current state the host machine has local ports that connect to each of the nodes. Meaning that nodes can be accessed via "http://localhost:port_number
"  
## Startup
Running the command:
```
python3 main.py config.json
```
Starts the program. Depending on how many nodes you have, the program will generate all of the appropriate Dockerfiles and account key files. It's recommended to have at least 2 nodes, with one being dedicated to deploying contracts. In it's current iteration, the "start_mining" function only has all nodes with a port number greater than 8485. This allows the node using port 8485 to deploy smart contracts and have the deployment be recorded into the blockchain.


![3_nodes](../images/Network_overview_3_nodes.jpg)


## Mining
Once the network has been set up, it's time to mine nodes

```
python3 nodes.py config.json start_mining
```
 
To stop mining:

```
python3 nodes.py config.json stop_mining
```

To check mining status of all current nodes:
```
python3 nodes.py config.json mine_check
```

## Balance
To check the balance of ether for all nodes:
```
python3 nodes.py config.json balance
```

## Look for transactions

To connect to a node and look for a particular transaction on the blockchain
```
python3 nodes.py config.json transaction
```

Then follow the prompts: one asks for the port to connect to the other asks for the transaction number.

# Deploying smart contract
To deploy a smart contract, you must use the node that corresponds with to localhost port 8545.

## Adding a network to Brownie:
```
brownie networks add Ethereum name_of_network 127.0.0.1:8545
```

This adds a network that connects directly to the node on localhost port 8545

## Deploying a contract with Browinie
Make sure to be in the geth-dev-main directory
```
brownie run scripts/token.py --network name_of_network
```

This will connect to your node at the port 8545 and as long as there is another node that is mining and adding blocks to the blockchain your contract will be deployed. If you look for transactions 


# Future plans:

- ### Create a docker container to act as the local host, that way the network is more portable
- ### have a way to designate specific nodes to mine without having the specified nodes in order
    - current iteration: nodes.py only has all  nodes with ports greater than 8545 (up to 8546 + number of nodes - 1)
    