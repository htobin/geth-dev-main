# Creating a Blockchain Network

## Introduction
In this project we're trying to create a simulated Ethereum network. In this project the following items will be simulated:
- The genesis node:
    - This node is what gives the blockchain an origin point. It also contains what's known as the genesis file. This block also allows other nodes on the system to detect each other.
- Account nodes:
    - These nodes are used to store a singular account which acts as a wallet. These nodes interact with the ethereum blockchain, they are able to commit transactions, mining work, deploy smart contracts, and interact with smart contracts.
- Smart contracts:
    - Bits of code that are available on the blockchain that can be utilized by nodes. **Smart contracts that will be included**
- Docker:
    - Allows for a single machine the create multiple instances of nodes.

## Step by step
### The bootnode:
- The bootnode is what connects allows each node to find each other when using the ethereum network, it is created. To create a bootnode you need three items:
    - Bootnode IP: The address used to find the Bootnode with the genesis data.
    - Bootnode Port: Used with the IP address for connecting to other nodes
    - Bootnode key: This key is the identifier that is used as a way to identify the bootnode
    - When intiating a node one of the commands used in geth is this format: 
        - **enode://$bootnodeId@$bootnodeIp:$bootnodePort**


 