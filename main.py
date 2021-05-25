# create a cryptocurrency called EdwCoin

import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4  # generate random uuid
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

    # replace longer chain for a shorter chain
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            # get chain from all nodes from the network
            # response = requests.get('http://127.0.0.1:5000/get_chain')
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                # if any other chain that is longer than current chain
                # replace the current chain with that longest chain
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
            # if longest chain is not none, replace and return true
            if longest_chain:
                self.chain = longest_chain
                return True
            return False


#part 2 - Mining our Blockchain

# Creating a Web App based on Flask
app = Flask(__name__)

# Create an address for the node on this port
node_address = str(uuid4()).replace('-', '')

# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
blockchain = Blockchain()


# CRUD get method
@app.route('/mine_block', methods=["GET"])
def mine_block():
    prev_block = blockchain.get_previous_block()
    prev_proof = prev_block['proof']

    # main mining work: find the expected_proof
    curr_proof = blockchain.proof_of_work(prev_proof)

    # create and add the correctly mined block to our chain
    prev_hash = blockchain.hash(prev_block)

    # give reward to the miner, the transaction fee
    blockchain.add_transaction(sender=node_address, receiver='Edward', amount=1)

    curr_block = blockchain.create_block(curr_proof, prev_hash)

    # return a json object
    response = {'message': 'Congratulations, you just mined a block!',
                'index': curr_block['index'],
                'timestamp': curr_block['timestamp'],
                'proof': curr_block['proof'],
                'prev_hash': curr_block['previous_hash'],
                'transactions:': curr_block['transactions'],
                }

    return jsonify(response), 200   # demo on postman:200 means everything is ok


# getting the full Blockchain
@app.route('/get_chain', methods=["GET"])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods=["GET"])
def is_valid():
    valid = blockchain.is_chain_valid(blockchain.chain)
    if valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Problem occurs. Blockchain is NOT valid'}

    return jsonify(response), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()   # get the json file from postman
    transaction_keys = ['sender', 'receiver', 'amount']
    # if json file not include each key, return error
    # all returns true if all items in an iterable returns true
    if not all(key in json for key in transaction_keys):
        return 'Missing components', 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201


# part3 - decentralizing our blockchain
if __name__ == '__main__':
    # Running the app on http://127.0.0.1:5000/
    # use postman to test
    app.run(host='0.0.0.0', port=5000)
