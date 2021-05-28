from coin import *

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

@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    # json = { "nodes": [http://127.0.0.1:5001, xxx, xxx] }
    nodes = json.get('nodes')  # list of address of the nodes
    if nodes is None:
        return "No node", 400
    for node_addr in nodes:
        blockchain.add_node(node_addr)
    response = {'message': 'all the nodes are now connected, it contains the following nodes',
                'total_nodes': list(blockchain.nodes)}
    return response


# part3 - decentralizing our blockchain
if __name__ == '__main__':
    # Running the app on http://127.0.0.1:5000/
    # use postman to test
    app.run(host='0.0.0.0', port=5000)