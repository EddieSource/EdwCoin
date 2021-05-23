# create a cryptocurrency called EdwCoin

import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# part 1 - build a blockchain
# add transactions
class Blockchain:
    def __init__(self):
        self.chain = []     # this is the main blockchain
        self.transactions = []  # this is the transaction list to be included in the current block
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()  # initialize an empty set for nodes for distribution purposes

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions
                 }
        self.transactions = []  # clear the transaction list, get it ready for next block
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # in real world this is changed to hash the data field(or with any other field) of the block object
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # check target value
            if hash_operation[0:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        # hash a block: generate the current hash code for the entire block: the finger print
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            curr_block = chain[block_index]
            # check if the previous_hash key of the current block equals to the previous block hash
            if curr_block['previous_hash'] != self.hash(previous_block):
                return False
            # check if the current proof of work reaches the target
            previous_proof = previous_block['proof']
            curr_proof = curr_block['proof']
            hash_operation = hashlib.sha256(str(curr_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # hash_operation = self.hash(curr_block)
            if hash_operation[:4] != '0000':
                return False
            previous_block = curr_block
            block_index += 1

        return True

    def add_transaction(self, sender, receiver, amount):
        # add a transaction to this transaction list
        # return the index of the upcoming new block
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    # take address of the node; e.g. 'http://127.0.0.1:5000/'
    def add_node(self, address):
        # url will return the parse of the address
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)   # the url including the port, '127.0.0.1:5000' for example

