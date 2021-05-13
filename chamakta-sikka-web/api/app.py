import time
import json
import requests
from flask import Flask, request
from uuid import uuid4
from flask_socketio import SocketIO, send, emit
import sys
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

app = Flask(__name__)

app.config['SECRET_KEY'] = 'csk'

socketIO = SocketIO(app, cors_allowed_origins="*")

# List of all users online
# users_online = []
PORT = sys.argv[1]
connected_users = []
key_pair = {}
public_key = None
private_key = None

class BlockChain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.transaction_limit = 10
        self.mine_genesis_block()

    def add_transaction(self, sender_private_key, sender_public_key, receiver_public_key, amount):
        #sign this data
        this_transaction = {
            'sender_public_key' : sender_public_key,
            'receiver_public_key' : receiver_public_key,
            'amount' : amount
        }
        signature = private_key.sign(
            json.dumps(this_transaction).encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        this_transaction['signature'] = signature.hex()
        self.transactions.append(this_transaction)
        self.broadcast_transaction(this_transaction)
        print("\n\n\nTransactions List: ")
        print(self.transactions)
        print("\n\n")
    
    def get_previous_block(self):
        return self.chain[-1]

    def hash_dict(self, dict_to_hash):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(json.dumps(dict_to_hash).encode('utf-8'))
        hash_value = digest.finalize()
        return hash_value.hex()

    def calculate_nonce(self, this_block):
        print('Calculating nonce...')
        while True:
            for i in range(1, 100000000):
                this_block['nonce'] = i
                this_block['timestamp'] = time.time()
                if self.hash_dict(this_block)[0:3] == '000':
                    print(f"\n\nNonce found: {i}")
                    print(f"Hash: {self.hash_dict(this_block)}\n\n")
                    return i    
        print("Not found")

    def mine_genesis_block(self):
        genesis_block = {
            'block_number' : 0
        }
        nonce = self.calculate_nonce(genesis_block)
        self.chain.append(genesis_block)

    def broadcast_transaction(self, transaction_to_broadcast):
        # send this transaction to all nodes
        for user in connected_users: 
            if str(user['PORT']) != PORT:
                requests.post('http://localhost:{0}/api/receive_transaction'.format(user['PORT']), json={"new_transaction": transaction_to_broadcast})

blockchain = BlockChain()

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/update_connected_users', methods=['POST'])
def update_connected_users():
    global connected_users
    all_users = request.get_json(force=True)
    print("----------------")
    # print(all_users)
    connected_users = all_users['all_users']
    print(connected_users)
    socketIO.emit('connected_users', connected_users, broadcast=True)
    print("----------------")
    return {'success' : 'yes'}

@app.route('/api/provide_keys', methods=['POST'])
def provide_keys():
    global key_pair, public_key, private_key
    key_pair_data = request.get_json(force=True)
    print("-----------------------")
    # print(all_users)
    key_pair = key_pair_data['public_private_keys']
    print(key_pair)
    private_key_pem = bytes.fromhex(key_pair['private_key'])
    public_key_pem =  bytes.fromhex(key_pair['public_key'])

    # doing some signature stuff
    private_key = crypto_serialization.load_pem_private_key(
        private_key_pem,
        password=None,
        backend=default_backend()
    )

    public_key = crypto_serialization.load_pem_public_key(
        public_key_pem,
        backend=default_backend()
    )

    socketIO.emit('provide_keys', key_pair, broadcast=True)

    return {'success' : 'yes'}


'''
{
    'amount' : 3000
}
'''
@app.route('/api/coin_base_transaction', methods=['POST'])
def coin_base_transaction():
    coin_base_data = request.get_json(force=True)
    print(coin_base_data)
    print(key_pair['public_key'])
    amount_coinbase = coin_base_data['amount']
    blockchain.add_transaction('COINBASE_PRI_KEY', 'COINBASE_PUB_KEY', key_pair['public_key'], amount_coinbase)
    #broadcast this transaction to all nodes
    return {'success': 'yes'}


@app.route('/api/receive_transaction', methods=['POST'])
def receive_transaction():
    transaction_data = request.get_json(force=True)
    # print(coin_base_data)
    # print(key_pair['public_key'])
    new_transaction = transaction_data['new_transaction']
    blockchain.transactions.append(new_transaction)
    print("\n\nRecieved Transactions:")
    print(blockchain.transactions)
    print("\n\n")
    #broadcast this transaction to all nodes
    return {'success': 'yes'}

@app.route('/api/perform_transaction', methods=['POST'])
def perform_transaction():
    transaction_details = request.get_json(force=True)
    transaction_parameters = ['receiver_public_key', 'amount']
    if not all (key in transaction_details for key in transaction_parameters):
        return {'success': 'no', 'error': 'Not valid body'}
    receiver_public_key = transaction_details['receiver_public_key']
    transaction_amount = transaction_details['amount']
    print("\n\nsender public key:")
    print(key_pair['public_key'])
    print("\n\n")
    blockchain.add_transaction(key_pair['private_key'], key_pair['public_key'], receiver_public_key, transaction_amount)
    #broadcast this transaction to all nodes
    return {'success': 'yes'}

@app.route('/api/mine_block', methods=['POST'])
def mine_block():
    transactions_list = blockchain.transactions
    # blockchain.transactions = []
    previous_block_hash = blockchain.hash_dict(blockchain.get_previous_block())
    timestamp = time.time()
    block_number = len(blockchain.chain)
    this_block = {
        'block_number': block_number,
        'timestamp': timestamp,
        'transactions_list': transactions_list,
        'previous_block_hash': previous_block_hash
    }
    nonce = blockchain.calculate_nonce(this_block)
    print(nonce)
    this_block['nonce'] = nonce
    blockchain.chain.append(this_block)

    print("\n\nBlocks:")
    print(json.dumps(blockchain.chain, sort_keys=False, indent=4))
    print("\n\n")

    return {'success': 'yes'}


@socketIO.on('connect')
def connected():
    print('Connected')

@socketIO.on('disconnect')
def disconnected():
    # isRemoved = removeUser(request.sid)
    # if isRemoved:
    #     emit('userRefresh', users_online, broadcast=True)
    print('Disconnected')

@socketIO.on("message")
def sendSomethign(msg):
    print(msg)
    send(msg, broadcast=True)
    return None


@socketIO.on("addNewUser")
def addNewUser(data):
    print(data['username'])
    user_to_add = {}
    user_to_add['username'] = data['username']
    user_to_add['sid'] = request.sid
    user_to_add['uuid'] = str(uuid4()).replace("-","")
    user_to_add['wallet_balance'] = int(data['initamount'])
    users_online.append(user_to_add)
    print(users_online)
    emit('userInfo', user_to_add, room=request.sid)
    emit("userRefresh", users_online, broadcast=True)
    return None


if __name__ == '__main__':
    socketIO.run(app, port = PORT)