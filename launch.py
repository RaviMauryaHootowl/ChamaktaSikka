import os
import threading
import requests

# Users list (with their port numbers)


# An api to get list of all instances (Clients can fetch from here)



def create_instance(port):
  os.system(f'python app.py {port}')

# Take input - kitne users chahiye (n)
# Launch n number of instances on different ports


t1 = threading.Thread(target=create_instance, args=(5000,))
t2 = threading.Thread(target=create_instance, args=(5001,))



t1.start()
t2.start()

all_users = [{
  'PORT' : 5000,
  'public_key' : 'asdfasdf'
},
{
  'PORT' : 5001,
  'public_key' : '463854afe'
}]

for user in all_users: 
  requests.post(f'http://localhost:{user['PORT']}/api/update_connected_users', all_users)

t1.join()
t2.join()

# Menu type 
'''
1. To close all clients
2. Close client by port number
3. Add new client
'''

# from cryptography.hazmat.primitives import serialization as crypto_serialization
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.backends import default_backend as crypto_default_backend
# from cryptography.hazmat.primitives.asymmetric import padding

# key = rsa.generate_private_key(
#     backend=crypto_default_backend(),
#     public_exponent=65537,
#     key_size=512
# )
# private_key_bytes = key.private_bytes(
#     crypto_serialization.Encoding.PEM,
#     crypto_serialization.PrivateFormat.PKCS8,
#     crypto_serialization.NoEncryption())
# public_key_bytes = key.public_key().public_bytes(
#     crypto_serialization.Encoding.OpenSSH,
#     crypto_serialization.PublicFormat.OpenSSH
# )

# print(type(key))
# print(type(key.public_key()))
# print(private_key_bytes)
# print(public_key_bytes)

# message = b"A message I want to sign"
# signature = key.sign(
#     message,
#     padding.PSS(
#         mgf=padding.MGF1(hashes.SHA256()),
#         salt_length=padding.PSS.MAX_LENGTH
#     ),
#     hashes.SHA256()
# )

# print(signature)

# public_key = key.public_key()
# public_key.verify(
#     signature,
#     message,
#     padding.PSS(
#         mgf=padding.MGF1(hashes.SHA256()),
#         salt_length=padding.PSS.MAX_LENGTH
#     ),
#     hashes.SHA256()
# )