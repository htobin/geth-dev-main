import argparse
import ipaddress

from yaml import parse
def ingest_config_file():
    parser = argparse.ArgumentParser(description='create docker compose file, directories for nodes, and Dockerfiles for nodes')
    parser.add_argument('config_file', help='keyfile that contains information about bootnode, amount of nodes, IP range for nodes, and the network ID')
    file = parser.parse_args()
    return file

def create_bootnode_data(key,enode,IP,port):
    data = {
        "nodehexkey": key,
        "enode": enode,
        "port": port,
        "ip": IP
    }
    return data

def create_bootnode(bnode_data):
    #nodehexkey string creation
    nodekeyhex_string = "nodekeyhex=" + bnode_data["nodehexkey"]
    bnode_port_string = bnode_data["port"]+":"+ bnode_data["port"] + "/udp"
    bnode_port_environment = "port="+bnode_data["port"]
    bootnode = {
        'hostname': 'geth-bootnode',
        'environment': [
                nodekeyhex_string,
                bnode_port_environment
            ],
            'build': {
                'context' :'./geth-bootnode'
            },
            'ports': [
                bnode_port_string
            ],
            'volumes':["bootnode:/root/.ethash"],
            'networks':{
                'chainnet':{
                    'ipv4_address':bnode_data["ip"]
                }
            }   
    }

    return bootnode

def create_nodes_wrapper(net_range, n_count, bnode_data, chain_id):
    #create start of IP
    end_of_ip_range = net_range.find("/")
    ip = net_range[:end_of_ip_range]
    ip_addr = ipaddress.ip_address(ip) + 2

    i=0
    rpc_port = 8545
    discover_port = 30302
    n_count = int(n_count)
    node_obj = {}
    while i < n_count:
        node = create_node(str(i),str(ip_addr), bnode_data, str(rpc_port), str(discover_port), str(chain_id))
        node_obj[node["hostname"]] = node
        rpc_port +=1
        discover_port +=1
        ip_addr +=1
        i+=1
    return node_obj
    

def create_node(num,node_ip, bnode_data, rpc, discover, net_id):
    node_name = "node_"+ num
    n_name= "geth-dev-" + node_name
    #environmental variables
    rpc_env_string = "rpcPort=" + rpc
    discover_env_string ="discoverPort=" + discover
    bnode_id_string = "bootnodeId=" + bnode_data["enode"]
    bnode_ip_string = "bootnodeIp=" + bnode_data["ip"]
    bnode_port_string = "bootnodePort=" + bnode_data["port"]
    network_id_string = "networkId=" + net_id

    #port string
    rpc_port_string = rpc+":"+ rpc
    discover_port_string = discover+ ":" + discover +"/udp"


    dockerfile_string = "./"+ n_name +"/Dockerfile"
    test_string = "wget http://localhost:" + rpc
    volume_string = "eth-data-"+num+":/root/.ethhash"

    node = {
        'hostname': n_name,
        'depends_on':['geth-bootnode'],
        'environment':[
            bnode_id_string,
            bnode_ip_string,
            rpc_env_string,
            discover_env_string,
            bnode_port_string,
            network_id_string
        ],
        'build':{
            'context': ".",
            'dockerfile': dockerfile_string
        },
        'container_name': n_name,
        'healthcheck':{
            'test': test_string,
            'interval':'2s',
            'timeout':'5s',
            'retries':'30'
        },
        'volumes':[
            volume_string
        ],
        'ports':[
            rpc_port_string,
            discover_port_string
        ],
        'networks':{
            'chainnet':{
                'ipv4_address':node_ip
            }
        }
    }
    return node

def create_network(net_range):
    network = {
        'chainnet':{
            'driver': 'bridge',
            'ipam':{
                'config':[{'subnet':net_range}]
            }
        }
    }   
    return network

def create_volumes(num_nodes):
    volumes = {}
    volumes["bootnode"] = None
    i = 0
    while i < int(num_nodes):
        volume_string = "eth-data-" + str(i)
        volumes[volume_string] = None
        i+=1
    return volumes