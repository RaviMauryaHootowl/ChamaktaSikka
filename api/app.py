import datetime
import copy
import json
import requests
from dotenv import dotenv_values
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import sys
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

app = Flask(__name__, static_folder="../build/static", template_folder="../build")

app.config['SECRET_KEY'] = 'csk'
config = dotenv_values("../.env")
print("\n\nRunning on mode {}\n\n".format(config['REACT_APP_MODE']))
socketIO = SocketIO(app, cors_allowed_origins="*")
CORS(app)

EMPTY_HASH = '0000000000000000000000000000000000000000000000000000000000000000'
COINBASE_PUB_KEY = 'COINBASE_PUB_KEY'
COINBASE_PRI_KEY = 'COINBASE_PRI_KEY'
PORT = sys.argv[1]
connected_users = []
key_pair = {}
public_key = None
private_key = None


'''
Blockchain Class
'''
class BlockChain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.transaction_limit = 10

    def add_transaction(self, sender_private_key, sender_public_key, sender_hash_public_key, receiver_public_key, amount, incentive):
        this_transaction = {
            'sender_public_key' : sender_public_key,
            'sender_hash_public_key': sender_hash_public_key,
            'receiver_public_key' : receiver_public_key,
            'amount' : amount,
            'incentive': incentive,
            'timestamp': datetime.datetime.now().isoformat()
        }
        this_transaction['transaction_hash'] = self.hash_dict(this_transaction, True)
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
        socketIO.emit('transactions', self.transactions, broadcast=True)
    
    def get_previous_block(self):
        return self.chain[-1]

    def hash_dict(self, dict_to_hash, debug):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(json.dumps(dict_to_hash, sort_keys=True).encode('utf-8'))
        hash_value = digest.finalize()
        return hash_value.hex()

    def calculate_nonce(self, this_block):
        while True:
            for i in range(1, 100000000):
                this_block['nonce'] = i
                this_block['timestamp'] = datetime.datetime.now().isoformat()
                if self.hash_dict(this_block, False)[0:3] == '000':
                    return i    
        print("Not found")

    def broadcast_transaction(self, transaction_to_broadcast):
        for user in connected_users: 
            if str(user['PORT']) != PORT:
                requests.post('http://localhost:{}/api/receive_transaction'.format(user['PORT']), json={"new_transaction": transaction_to_broadcast})


'''
Creating Instance of the Blockchain
'''
blockchain = BlockChain()


'''
App routes
'''

if config['REACT_APP_MODE'] == 'PRODUCTION':
    @app.route("/")
    def server_page():
        return render_template('index.html')

@app.route('/api/update_connected_users', methods=['POST'])
def update_connected_users():
    global connected_users
    all_users = request.get_json(force=True)
    connected_users = all_users['all_users']
    socketIO.emit('connected_users', connected_users, broadcast=True)
    return {'success' : 'yes'}

def ping_all_users_for_blockchain_update():
    for user in connected_users: 
        if str(user['PORT']) != PORT:
            requests.post('http://localhost:{}/api/receive_blockchain_update_ping'.format(user['PORT']))

@app.route('/api/provide_keys', methods=['POST'])
def provide_keys():
    global key_pair, public_key, private_key
    key_pair_data = request.get_json(force=True)
    key_pair = key_pair_data['public_private_keys']
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


@app.route('/api/coin_base_transaction', methods=['POST'])
def coin_base_transaction():
    coin_base_data = request.get_json(force=True)
    amount_coinbase = coin_base_data['amount']
    is_done = perform_coin_base_transaction(amount_coinbase)
    #broadcast this transaction to all nodes
    return {'success': 'yes'}

def perform_coin_base_transaction(amount_coinbase):
    blockchain.add_transaction(COINBASE_PRI_KEY, COINBASE_PUB_KEY, COINBASE_PUB_KEY, key_pair['hash_public_key'], amount_coinbase, 0)
    return True

@app.route('/api/receive_transaction', methods=['POST'])
def receive_transaction():
    transaction_data = request.get_json(force=True)
    new_transaction = transaction_data['new_transaction']
    blockchain.transactions.append(new_transaction)
    socketIO.emit('transactions', blockchain.transactions, broadcast=True)
    #broadcast this transaction to all nodes
    return {'success': 'yes'}

@app.route('/api/perform_transaction', methods=['POST'])
def perform_transaction():
    transaction_details = request.get_json(force=True)
    transaction_parameters = ['receiver_public_key', 'amount', 'incentive']
    if not all (key in transaction_details for key in transaction_parameters):
        return {'success': 'no', 'error': 'Not valid body'}
    receiver_public_key = transaction_details['receiver_public_key']
    if key_not_valid(receiver_public_key):
        return {'success': 'no', 'message': "Receiver Key not valid"}, 400
    transaction_amount = transaction_details['amount']
    transaction_incentive = transaction_details['incentive']
    blockchain.add_transaction(key_pair['private_key'], key_pair['public_key'], key_pair['hash_public_key'], receiver_public_key, transaction_amount, transaction_incentive)
    return {'success': 'yes'}

def key_not_valid(receiver_public_key):
    for u in connected_users:
        if u['hash_public_key'] == receiver_public_key:
            return False
    return True


@app.route('/api/mine_block', methods=['POST'])
def mine_block():
    transactions_list = blockchain.transactions
    blockchain.transactions = []
    previous_block_hash = 0
    block_number = len(blockchain.chain)
    if block_number > 0:
        previous_block_hash = blockchain.hash_dict(blockchain.get_previous_block(), False)
    else:
        previous_block_hash = EMPTY_HASH
    timestamp = datetime.datetime.now().isoformat()
    # Check for each transaction if the sender has the required amount
    valid_transactions = []
    for transact in transactions_list:
        if len(valid_transactions) >= 10:
            break
        isPos = False
        if transact['sender_public_key'] == COINBASE_PUB_KEY:
            isPos = True
        else:
            res = requests.post('http://localhost:{0}/api/check_and_reduce_wallet'.format(public_key_to_port(transact['sender_hash_public_key'])), json=transact).json()
            isPos = res['isPos']
        
        if isPos:
            requests.post('http://localhost:{0}/api/increase_wallet'.format(public_key_to_port(transact['receiver_public_key'])), json=transact)
            key_pair['wallet'] += transact['incentive']
            valid_transactions.append(transact)
        else:
            blockchain.transactions.append(transact)   #rejected transaction
    emit_wallet_info()
    if len(valid_transactions) > 0:
        this_block = {
            'block_number': block_number,
            'timestamp': timestamp,
            'miner_hash_public_key': key_pair['hash_public_key'],
            'transactions_list': valid_transactions,
            'previous_block_hash': previous_block_hash
        }
        nonce = blockchain.calculate_nonce(this_block)
        blockchain.chain.append(this_block)
        ping_all_users_for_blockchain_update()

    socket_emit_chain()
    socketIO.emit('transactions', blockchain.transactions, broadcast=True)
    return {'success': 'yes'}

@app.route('/api/receive_blockchain_update_ping', methods=['POST'])
def receive_blockchain_update_ping():
    for user in connected_users: 
        if str(user['PORT']) != PORT:
            res = requests.get('http://localhost:{}/api/get_blockchain_and_transactions'.format(user['PORT'])).json()
            users_blockchain = res['chain']
            if len(blockchain.chain) <= len(users_blockchain):
                blockchain.chain = users_blockchain
                blockchain.transactions = res['transactions']
    socket_emit_chain()
    socketIO.emit('transactions', blockchain.transactions, broadcast=True)
    return {'success': 'yes'}

@app.route('/api/check_and_reduce_wallet', methods=['POST'])
def check_and_reduce_wallet():
    transact = request.get_json(force=True)
    if key_pair['wallet'] >= (transact['amount'] + transact['incentive']):
        key_pair['wallet'] -= (transact['amount'] + transact['incentive'])
        emit_wallet_info()
        return {'isPos': True}    
    return {'isPos': False}

@app.route('/api/increase_wallet', methods=['POST'])
def increase_wallet():
    transact = request.get_json(force=True)
    key_pair['wallet'] += transact['amount']
    emit_wallet_info()
    return {'isPos': False}

@app.route('/api/get_blockchain_and_transactions', methods=['GET'])
def get_blockchain_and_transactions():
    return {'chain': blockchain.chain, 'transactions': blockchain.transactions}



'''
Socket listen ports & Utilities
'''


@socketIO.on('connect')
def connected():
    print('Connected')

@socketIO.on('disconnect')
def disconnected():
    print('Disconnected')

@socketIO.on("refresh_connected_users")
def refresh_connected_users():
    socketIO.emit('connected_users', connected_users, broadcast=True)
    return None

@socketIO.on("refresh_keys")
def refresh_keys():
    socketIO.emit('provide_keys', key_pair, broadcast=True)
    return None

@socketIO.on("refresh_transactions")
def refresh_transactions():
    socketIO.emit('transactions', blockchain.transactions, broadcast=True)
    return None

@socketIO.on("refresh_blockchain")
def refresh_blockchain():
    socket_emit_chain()
    return None

def emit_wallet_info():
    socketIO.emit('provide_keys', key_pair, broadcast=True)

def socket_emit_chain():
    chain_with_block_hash = []
    for block in blockchain.chain:
        current_block = copy.deepcopy(block)
        current_block['block_hash'] = blockchain.hash_dict(current_block, True)
        chain_with_block_hash.append(current_block)
    socketIO.emit('blockchain', chain_with_block_hash, broadcast=True)

def public_key_to_port(public_key_to_convert):
    for user in connected_users:
        if user['hash_public_key'] == public_key_to_convert:
            return user['PORT']
    return None

if __name__ == '__main__':
    socketIO.run(app, port = PORT)