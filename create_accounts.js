'use strict';

const fs= require('fs');
const { exit } = require('process');
const Web3= require('web3');

//read in config file
function read_config_file(config_file){
    let raw;
    try{
        raw = fs.readFileSync(config_file);
    } catch(err){
        console.log(err);
    }
    let data = JSON.parse(raw);
    return data
}

function create_port_numbers(node_count){
    let port_numbers = [];
    let i = 0;
    let first_port = 8545;
    while(i < node_count){
        port_numbers.push(first_port + i);
        i++;
    }
    return port_numbers;
}

function create_connection_strings(port_numbers){
    let connection_strings = [];
    port_numbers.forEach(port => {
        let current_string = "http://localhost:" + port.toString();
        connection_strings.push(current_string);
    });
    return connection_strings
}

function create_node_connections(connection_strings){
    let node_connections = new Map();
    connection_strings.forEach(string =>{     
        node_connections.set(string.slice(-4),new Web3(string)); 
    });
    return node_connections;
}


function access_nodes(nodes){
    nodes.forEach(function(node_obj,node_name){
        node_obj.eth.net.isListening().then(
            success => {success}
           ,rejected => {console.log(node_name +"|Error:\n\t "+ rejected.message)}
        );
    });
}

function create_accounts(nodes){
    nodes.forEach(function(node_obj,node_name){
        console.log(node_name+" account being created");
        node_obj.eth.personal.newAccount("pass").then(console.log);
    });
}


function connect_to_nodes(){
    //read in the data
    let config_data = read_config_file(process.argv[2]);
    //function to create port numbers to connect to nodes
    let port_numbers = create_port_numbers(config_data["node_count"]);
    //function to create strings to connect to nodes
    let connection_strings = create_connection_strings(port_numbers);
    let nodes = create_node_connections(connection_strings);
    //node objects are connected, create accounts
    return nodes
}
let nodes = connect_to_nodes();
create_accounts(nodes);

