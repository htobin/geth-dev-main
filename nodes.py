import argparse
import json
from web3 import Web3

def arguments():
    parser = argparse.ArgumentParser(description='create docker compose file, directories for nodes, and Dockerfiles for nodes')
    parser.add_argument('config_file', help='keyfile that contains information about bootnode, amount of nodes, IP range for nodes, and the network ID')
    parser.add_argument('function',nargs='?',help='function to indicate which')
    arguments = parser.parse_args()
    return arguments

def read_config_file(config_file):
    try:
        with open(config_file) as config_f:
            config_data = json.load(config_f)
    except OSError:
        print(f"could not open {config_file} file")
        exit()
    return config_data

def create_node_names(config_node_count):
    node_names = []
    i = 0
    first_port = 8545
    while i < int(config_node_count):
        node_names.append(str(first_port + i))
        i+=1
    return node_names

def create_node_obj(node_names):
    node_objs ={}
    for name in node_names:
        current_string = "http://localhost:" + name
        node_objs[name] =  Web3(Web3.HTTPProvider(current_string))
    return node_objs


def connect_to_nodes(args):
    config_data = read_config_file(args.config_file)
    node_names = create_node_names(config_data["node_count"])
    node_objs = create_node_obj(node_names)
    return node_objs

def connection_check(nodes):
    for name in nodes.keys():
        if nodes[name].isConnected():
            print(f"{name} is connected")
        else:
            print(f"{name} is not connected")

def create_accounts(nodes):
    for name in nodes.keys():
        nodes[name].personal.newAccount("pass")

def account_check(nodes):
    for name in nodes.keys():
        print(f"{name}:  account: {nodes[name].eth.accounts[0]}")
        print(f"{name}: coinbase: {nodes[name].eth.coinbase}")

def start_mining(nodes):
    for name in nodes.keys():
        print(f"{name}: starting to mine")
        nodes[name].miner.start(1)
        if(nodes[name].eth.mining):
            print(f"{name} is mining")
        else:
            print(f"{name} is not mining")

def stop_mining(nodes):
    for name in nodes.keys():
        print(f"{name}: mining will stop")
    nodes[name].geth.miner.stop()
    if(nodes[name].eth.mining):
        print(f"{name} is still mining")
    else:
        print(f"{name} is not mining")


if __name__ == "__main__":
    args = arguments()
    nodes = connect_to_nodes(args)
    connection_check(nodes)
    if args.function =="create_accounts":
        create_accounts(nodes)
        account_check(nodes)
    if args.function =="start_mine":
        start_mining(nodes)
    if args.function =="stop_mine":
        start_mining(nodes)

    



