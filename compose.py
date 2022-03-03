# File: compose.py
# Description: Contains functions that create the Docker compose file
import argparse
import ipaddress

from yaml import parse


# Function: ingest_config_file
# Description: Argument error checking and handler
# Return: the argument being passed in

def ingest_config_file():
    parser = argparse.ArgumentParser(
        description='create docker compose file, directories for nodes, and Dockerfiles for nodes')
    parser.add_argument('config_file',
                        help='keyfile that contains information about bootnode, amount of nodes, IP range for nodes, '
                             'and the network ID')
    file = parser.parse_args()
    return file


# Function: create_bootnode_data
# Description: Takes in the boot node data, and puts it into a dictionary that's easy to reference
# Arguments:
#          key: hex key of the boot node
#          enode: the enode address so that way other nodes can connect to the boot node
#          IP: IP address of the boot node
#          port: discover port of the boot node   
# Return: The argument being passed in

def create_bootnode_data(key, enode, IP, port):
    data = {
        "nodehexkey": key,
        "enode": enode,
        "port": port,
        "ip": IP
    }
    return data


# Function: create_bootnode
# Description: Parses boot node data and creates the boot node Docker compose section
# Arguments:
#          bnode_data: dictionary with information of the boot node
# Return: bootnode: boot node portion of the Docker compose file

def create_bootnode(bnode_data):
    # nodehexkey string creation
    nodekeyhex_string = "nodekeyhex=" + bnode_data["nodehexkey"]
    bnode_port_string = bnode_data["port"] + ":" + bnode_data["port"] + "/udp"
    bnode_port_environment = "port=" + bnode_data["port"]
    bootnode = {
        'hostname': 'geth-bootnode',
        'environment': [
            nodekeyhex_string,
            bnode_port_environment
        ],
        'build': {
            'context': './geth-bootnode'
        },
        'ports': [
            bnode_port_string
        ],
        'volumes': ["bootnode:/root/.ethash"],
        'networks': {
            'chainnet': {
                'ipv4_address': bnode_data["ip"]
            }
        }
    }

    return bootnode


# Function: create_nodes_wrapper
# Description: Creates the node dictionary keys and values
# Arguments:
#          net_range: range of the IP addresses that will be used for all nodes
#          n_count: number of nodes that will be created
#          bnode_data: dictionary with information of the boot node
#          chain_id: ID of the blockchain where work will be commited
# Return: node_obj: Dictionary of all nodes and the information about each individual node

def create_nodes_wrapper(net_range, n_count, bnode_data, chain_id):
    # create the base IP address for the first node that's not a boot node
    end_of_ip_range = net_range.find("/")
    ip = net_range[:end_of_ip_range]
    ip_addr = ipaddress.ip_address(ip) + 2

    # counter for incrementing through the amount of nodes
    i = 0

    # ports for the first node that's not a boot node
    rpc_port = 8545
    discover_port = 30302

    # total nodes
    n_count = int(n_count)
    node_obj = {}

    while i < n_count:
        node = create_node(str(i), str(ip_addr), bnode_data, str(rpc_port), str(discover_port), str(chain_id))
        node_obj[node["hostname"]] = node

        # increment ports, IP address, and the node name by 1
        rpc_port += 1
        discover_port += 1
        ip_addr += 1
        i += 1
    return node_obj


# Function: create_node
# Description: Creates the current node's Docker compose portion
# Arguments:
#          net_range: range of the IP addresses that will be used for all nodes
#          n_count: number of nodes that will be created
#          bnode_data: dictionary with information of the boot node
#          chain_id: ID of the blockchain where work will be commited
# Return: node: Docker compose portion for the node

def create_node(num, node_ip, bnode_data, rpc, discover, net_id):
    node_name = "node_" + num
    n_name = "geth-dev-" + node_name

    # Docker environment variables for the node
    rpc_env_string = "rpcPort=" + rpc
    discover_env_string = "discoverPort=" + discover
    bnode_id_string = "bootnodeId=" + bnode_data["enode"]
    bnode_ip_string = "bootnodeIp=" + bnode_data["ip"]
    bnode_port_string = "bootnodePort=" + bnode_data["port"]
    network_id_string = "networkId=" + net_id

    # ports
    rpc_port_string = rpc + ":" + rpc
    discover_port_string = discover + ":" + discover + "/udp"

    dockerfile_string = "./" + n_name + "/Dockerfile"
    test_string = "wget http://localhost:" + rpc
    volume_string = "eth-data-" + num + ":/root/.ethhash"

    node = {
        'hostname': n_name,
        'depends_on': ['geth-bootnode'],
        'environment': [
            bnode_id_string,
            bnode_ip_string,
            rpc_env_string,
            discover_env_string,
            bnode_port_string,
            network_id_string
        ],
        'build': {
            'context': ".",
            'dockerfile': dockerfile_string
        },
        'container_name': n_name,
        'healthcheck': {
            'test': test_string,
            'interval': '2s',
            'timeout': '5s',
            'retries': '30'
        },
        'volumes': [
            volume_string
        ],
        'ports': [
            rpc_port_string,
            discover_port_string
        ],
        'networks': {
            'chainnet': {
                'ipv4_address': node_ip
            }
        }
    }
    return node


# Function: create_network
# Description: Creates the network portion of the Docker compose file
# Arguments:
#          net_range: range of the IP addresses that will be used for all nodes
# Return: network: network portion of the Docker compose file

def create_network(net_range):
    network = {
        'chainnet': {
            'driver': 'bridge',
            'ipam': {
                'config': [{'subnet': net_range}]
            }
        }
    }
    return network


# Function: create_volumes
# Description: Creates the network portion of the Docker compose file
# Arguments:
#          num_nodes: amount of wallet nodes that will be created
# Return: volumes: volume portion of the Docker compose file

def create_volumes(num_nodes):
    volumes = {}
    volumes["bootnode"] = None
    i = 0
    while i < int(num_nodes):
        volume_string = "eth-data-" + str(i)
        volumes[volume_string] = None
        i += 1
    return volumes
