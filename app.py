import hashlib
import json
import datetime
import functools
from flask import Flask, jsonify, request,render_template
import requests
from uuid import uuid4
from urllib.parse import urlparse
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import base64

# class User:
#     def __init__(self, name):
#         self.name = name
#         self.details = self.rsakeys()
#         self.wallet = 0
    
#     def rsakeys():
#         length = 1024
#         privatekey = RSA.generate(length, Random.new().read)
#         publickey = privatekey.publickey()
#         user = {'privateKey':privatekey,'publicKey':publickey}
#         return user

class BlockChain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.transaction_limit = 10
        self.create_block(proof = 1, previous_hash = "0")

    def update_mempool_afterBlock(self):
        network = self.nodes
        for node in network:
            res = requests.post(f"https://{node}/update_mempool_afterBlock",data = {"mempool":self.transactions})
            if res.status_code == 201:
                continue
            else :
                print("Error updating mempool on node {0} : {1}".format(node,res.reason))

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "transactions": self.transactions[:self.transaction_limit],
            "previous_hash": previous_hash
        }
        self.transactions = self.transactions[self.transaction_limit :]
        self.chain.append(block)
        self.update_mempool_afterBlock()
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        proof = 1
        check_proof = False
        while check_proof == False:
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[0:4] == "0000":
                check_proof = True
            else:
                proof += 1

        return proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return  hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False

            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[0:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True

    def broadcast_transaction(self, sender, receiver, amount):
        network = self.Nodes
        Tobj = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        }
        for node in network:
            res = requests.post(f"https://{node}/update_mempool",data = Tobj)
            if res.status_code == 201:
                continue
            else :
                print("Error updating mempool on node {0} : {1}".format(node,res.reason))

    def check_balance(Self,sender_name):
        def check(x):
            if x.sender == sender_name:
                return x.amount
            else:
                return 0
        return reduce(lambda x,y: x + y, map(check,self.transactions))
        
    def add_transaction(self, sender, signature, publickey, receiver, amount):
        # signature = sign(private_key,{
        #     "sender": sender,
        #     "receiver": receiver,
        #     "amount": amount
        # })
        
        if amount <= check_balance(sender): 
            data= {"sender": sender,
                "receiver": receiver,
                "amount": amount}
            valid = verify(publickey,data,signature)
            if valid :
                self.transactions.append({
                    "sender": sender,
                    "receiver": receiver,
                    "amount": amount,
                    'signature': signature 
                })
                self.broadcast_transaction(sender, receiver, amount)
            else:
                print("Verification failed!")
        else:
            print("Transaction invalid due to insufficient balance!")

        # return self.get_previous_block()["index"] + 1


    def add_node(self, address):
        parsed_address = urlparse(address)
        self.nodes.add(parsed_address.netloc)

    def replace_with_longestchain(self):
        network = self.nodes
        longest_chain = None
        max_length_of_chain = len(self.chain)
        for node in network:
            res = requests.get(f"https://{node}/get_chain")
            if res.status_code == 200:
                length = res.json()["length"]
                chain = res.json()["chain"]
                if length > max_length_of_chain and self.is_chain_valid(chain):
                    max_length_of_chain = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True

        return False
    
    def sign(privatekey, data):
        return base64.b64encode(str((privatekey.sign(data, ''))[0]).encode())

    def verify(publickey, data, sign):
        return publickey.verify(data, (int(base64.b64decode(sign)),))


app = Flask(__name__)

node_address = str(uuid4()).replace("-","")

blockchain = BlockChain()


# @app.route("/")
# def home():
#     return render_template("index.html", chain = blockchain.chain)

#Form for carrying out transaction
# @app.route("/transaction")
# def transaction():
#     return render_template("transaction.html")


@app.route("/mine_block", methods = ["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address,receiver = "Me",amount = 12)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        "message": "It's so easy to mine a block. Here are your 12.5 Shrute bucks",
        "index":block["index"],
        "timestamp":block["timestamp"],
        "proof":block["proof"],
        "transactions":block["transactions"],
        "previous_hash":block["previous_hash"]
    }
    return jsonify(response), 200
    # return render_template("index.html", chain = blockchain.chain)

@app.route("/get_chain", methods = ["GET"])
def get_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route("/is_valid", methods = ["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response : {"message": "The BlockChain is valid."}
    else:
        response = {"message": "Looks like we messed up, the chain in invalid."}
    return jsonify(response), 200

@app.route("/add_transaction", methods = ["POST"])
def add_transaction():
    data = request.get_data()
    print(data)
    transaction_parameters = ["sender","receiver","amount"]
    if not all (key in data for key in transaction_parameters):
        return "You might have have missed some input fields."
    blockchain.add_transaction(data["sender"], data["receiver"], data["amount"])
    # res = {
    #     "message":f"The transaction will be added to the block no. {index}"
    # }
    res = {
        "message": "transaction added to our mempool"
        }
    return jsonify(res), 201
    # return render_template("index.html", chain = blockchain.chain)

@app.route("/update_mempool", methods = ["POST"])
def update_mempool(self):
    data = request.get_data()
    self.transactions.append({
        "sender": data["sender"],
        "receiver": data["receiver"],
        "amount": data["amount"]
    })
    res = {
        "message": "transaction added to mempool"
        }
    return jsonify(res), 201

@app.route("/update_mempool_afterBlock", methods = ["POST"])
def update_mempool_afterBlock(self):
    data = request.get_data()
    self.transactions = data["mempool"]
    res = {
        "message": "mempool updated"
        }
    return jsonify(res), 201

@app.route("/connect_node", methods = ["POST"])
def connect_node():
    data = request.get_json()
    nodes = data.get("nodes")
    if nodes is None:
        return "There are no nodes", 400
    for node in nodes:
        blockchain.add_node(node)
    res = {
        "message": "Nodes connected.",
        "Total_nodes": list(blockchain.nodes)
    }
    return jsonify(res), 201

@app.route("/replace_chain", methods = ["GET"])
def replace_chain():
    is_chain_replaced = blockchain.replace_with_longestchain()
    if is_chain_replaced:
        response = {"message": "The nodes had different chains so the chains were changed with the longest one.","new_chain": blockchain.chain}
    else:
        response = {
            "message": "No need to update the chain.",
            "chain": blockchain.chain
            }
    return jsonify(response), 200
app.run(host = '0.0.0.0', port = 5000)
