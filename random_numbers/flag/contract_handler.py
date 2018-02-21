from solc import compile_source
# web3 is needed to interact with eth contracts
from web3 import Web3, HTTPProvider, IPCProvider, TestRPCProvider
# we'll use ConciseContract to interact with our specific instance of the contract
from web3.contract import ConciseContract

from os import path
import json
import pickle
from pprint import pprint
import web3

url = 'http://localhost:8545'

class ContractHandler:
    def __init__(self):
        # Load contract configuration
        provider = HTTPProvider(url)
        self.eth_provider = Web3(provider).eth

        if not path.exists("configuration.p"):
            raise ValueError('Cannot find configuration.p')

        configuration = pickle.load( open( "configuration.p", "rb" ) )
        print(configuration)
        contract_address = configuration['contract_address'];
        print('*****\tcontract address {}'.format(contract_address))
        print('*****\tabi path {}'.format(configuration['abi_path']))
        print('*****\tcoinbase {}'.format(self.eth_provider.coinbase))
        with open(configuration['abi_path'], 'rb') as abi_definition:
            abi = json.load(abi_definition)
            print('*****\tcontract_abi.json loaded')
        self.contract_instance = self.eth_provider.contract(abi=abi,
                                                            address=contract_address,
                                                            ContractFactoryClass=ConciseContract)

        self.transaction_details = {
                'from': self.eth_provider.accounts[0],
                'gasPrice': 1,
                'gasLimit': 10000000,
                'value': 0}

    def placeBet(self):
        #self.contract_instance.placeBet(int(userChosenNumber), transact=self.transaction_details)
        self.contract_instance.placeBet(transact=self.transaction_details)

    def getWinningNumber(self):
        winningNumber = self.contract_instance.getWinningNumber()
        return winningNumber
