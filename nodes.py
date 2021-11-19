import argparse
import json
from web3 import Web3
import sys

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
        nodes[name].geth.personal.newAccount("pass")

def account_check(nodes):
    for name in nodes.keys():
        print(f"{name}:  account: {nodes[name].eth.accounts[0]}")
        print(f"{name}: coinbase: {nodes[name].eth.coinbase}")

def start_mining(nodes):
    i = 1
    while i < len(nodes):
        name = str(8545+i)
        print(f"{name}: starting to mine")
        nodes[name].geth.miner.start(2)
        if(nodes[name].eth.mining):
            print(f"{name} is mining")
        else:
            print(f"{name} is not mining")
        i+=1

def check_transactions(nodes):
    node = input("Please enter node port number: ")
    transaction = input("Please enter transaction number: ")
    print(f"connecting to port: {node}, looking for {transaction}")
    receipt =nodes[str(node)].eth.get_transaction_receipt(str(transaction)) 
    if receipt ==  False:
        print("could not find transaction")
    else: 
         raw = Web3.toJSON(receipt)
         parsed = json.loads(raw)
         print(json.dumps(parsed, indent=2))



def stop_mining(nodes):
    for name in nodes.keys():
        print(f"{name}: mining will stop")
        nodes[name].geth.miner.stop()
        if(nodes[name].eth.mining):
            print(f"{name} is still mining")
        else:
            print(f"{name} is not mining")

def unlock_accounts(nodes):
    for name in nodes.keys():
        self= nodes[name]
        account_to_unlock = self.geth.personal.list_accounts()[0]
        status = self.geth.personal.unlock_account(account_to_unlock, "pass")
        if status:
            print(f"{name} is unlocked")
        else:
            print(f"{name} is not unlocked")

def list_balance(nodes):
    for name in nodes.keys():
        self= nodes[name]
        account = self.geth.personal.list_accounts()[0]
        status = self.eth.get_balance(account)
        if status:
            print(f"{name} has {status}")
        else:
            print(f"could not get balance of {name}")

def still_mining(nodes):
    for name in nodes.keys():
        if(nodes[name].eth.mining):
            print(f"{name} is still mining")
        else:
            print(f"{name} is not mining")

if __name__ == "__main__":
    args = arguments()
    nodes = connect_to_nodes(args)
    #connection_check(nodes)
    if args.function =="create_accounts":
        create_accounts(nodes)
        account_check(nodes)
    if args.function =="start_mine":
        start_mining(nodes)
    if args.function =="stop_mine":
        stop_mining(nodes)
    if args.function =="unlock":
        unlock_accounts(nodes)
    if args.function =="mine_check":
        still_mining(nodes)
    if args.function =="balance":
        list_balance(nodes)
    if args.function =="transaction":
        check_transactions(nodes)

    



