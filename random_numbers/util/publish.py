#!/usr/bin/env python3

import json
import pdb
import web3
import time
import sys
import os.path
import pickle
import argparse

from web3 import Web3, HTTPProvider, IPCProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract

url = 'http://localhost:8545'

def connect():
    provider = HTTPProvider(url)
    eth_provider = Web3(provider).eth
    if eth_provider is None:
        return None;

    return eth_provider;

def contract(sol_path, config_path):
    eth_provider = connect();
    if eth_provider is None:
        print ('Cannot connect to ethereum provider.')
        return;

    if not os.path.exists(sol_path):
        print ('Cannot file path {}'.format(path));
        return;

    with open(sol_path) as file:
        source_code = file.readlines()

    # compile the contract
    compiled_code = compile_source(''.join(source_code))
    contract_name = os.path.splitext(os.path.basename(sol_path))[0]

    print('Compiling {}'.format(sol_path))
    # lets make the code a bit more readable by storing the values in variables
    contract_bytecode = compiled_code[f'<stdin>:{contract_name}']['bin']
    contract_abi = compiled_code[f'<stdin>:{contract_name}']['abi']

    with open( contract_name + '.abi', 'w+', encoding="utf8") as f:
        #pickle.dump(contract_abi, f)
        print('writing {}'.format(contract_name + '.abi'))
        json.dump(contract_abi, f)

    # create a contract factory. we'll use this to deploy any number of
    # instances of the contract to the chain
    contract_factory = eth_provider.contract(
        abi=contract_abi,
        bytecode=contract_bytecode,
    )

    # we'll use one of our default accounts to deploy from. every write to the chain requires a
    # payment of ethereum called "gas". if we were running an actual test ethereum node locally,
    # then we'd have to go on the test net and get some free ethereum to play with. that is beyond
    # the scope of this tutorial so we're using a mini local node that has unlimited ethereum and
    # the only chain we're using is our own local one
    default_account = eth_provider.accounts[0]
    # every time we write to the chain it's considered a "transaction". every time a transaction
    # is made we need to send with it at a minimum the info of the account that is paying for the gas
    transaction_details = {
        'from': default_account,
    }

    print('Deploying contract...')
    print('\n======INFO=====')
    # here we deploy the smart contract
    # two things are passed into the deploy function:
    #   1. info about how we want to deploy to the chain
    #   2. the arguments to pass the smart contract constructor
    # the deploy() function returns a transaction hash. this is like the id of the
    # transaction that initially put the contract on the chain

    transaction_hash = contract_factory.deploy(
        # the bare minimum info we give about the deployment is which ethereum account
        # is paying the gas to put the contract on the chain
        transaction=transaction_details,
    )

    print('TX hash: {}'.format(str(transaction_hash)))

    # if we want our frontend to use our deployed contract as it's backend, the frontend
    # needs to know the address where the contract is located. we use the id of the transaction
    # to get the full transaction details, then we get the contract address from there
    transaction_receipt = eth_provider.getTransactionReceipt(transaction_hash)
    contract_address = transaction_receipt['contractAddress']

    print('TX Receipt: {}'.format(str(transaction_receipt)))
    print('Contract address: {}'.format(str(contract_address)))
    print('======INFO=====')

    dir_path = os.path.dirname(os.path.realpath(__file__))

    configuration = dict()
    configuration['contract_address'] = str(contract_address)
    configuration['abi_path'] = os.path.join(dir_path, contract_name + '.abi')

    pickle.dump( configuration, open( os.path.join(config_path, 'configuration.p'), "wb" ) )

    contract_instance = eth_provider.contract(
        abi=contract_abi,
        address=contract_address,
        ContractFactoryClass=ConciseContract,
    )

    transaction_details = {
        'from': eth_provider.accounts[0]
    }

    while True:
        contract_instance.spam(transact=transaction_details)
        print('spamming network!')
        time.sleep(0.8)

def usage():
    print ('publish.py [contact sol file path] [configuration output path]');

def main():
    parser = argparse.ArgumentParser(description='Casino Contract publishing script')

    parser.add_argument('-i', '--input', action='store', dest='sol_path', required=True, help='sol file')
    parser.add_argument('-o', '--output', action='store', dest='config_path', required=True, help='output path of configuration.p')
    args = parser.parse_args()

    contract(args.sol_path, args.config_path)

if __name__ == "__main__":
    main()
# pdb.set_trace()
