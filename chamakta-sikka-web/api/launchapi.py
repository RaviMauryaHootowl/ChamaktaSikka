import os
import threading
import requests
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding


all_users = []
all_users_private_keys = []

for i in [5000, 5001]:
  key = rsa.generate_private_key(
      backend=default_backend(),
      public_exponent=65537,
      key_size=512)

  private_key_pem = key.private_bytes(
      crypto_serialization.Encoding.PEM,
      crypto_serialization.PrivateFormat.PKCS8,
      crypto_serialization.NoEncryption())

  public_key_pem = key.public_key().public_bytes(
      encoding=crypto_serialization.Encoding.PEM,
      format=crypto_serialization.PublicFormat.SubjectPublicKeyInfo)


  # print(type(private_key_pem))

  # pkString = f'{private_key_pem}'
  # # doing some signature stuff
  # private_key = crypto_serialization.load_pem_private_key(
  #     bytes.fromhex(private_key_pem.hex()),
  #     password=None,
  #     backend=default_backend()
  # )

  # print(type(private_key))

  all_users.append({
    'PORT': i,
    'public_key': public_key_pem.hex()
  })

  all_users_private_keys.append({
    'PORT': i,
    'private_key': private_key_pem.hex(),
    'public_key': public_key_pem.hex()
  })


for user in all_users: 
  requests.post('http://localhost:{0}/api/update_connected_users'.format(user['PORT']), json={"all_users": all_users})

for user in all_users_private_keys:
  requests.post('http://localhost:{0}/api/provide_keys'.format(user['PORT']), json={"public_private_keys": user})



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



# Users list (with their port numbers)


# An api to get list of all instances (Clients can fetch from here)



# def create_instance(port):
#   os.system(f'python app.py {port}')

# # Take input - kitne users chahiye (n)
# # Launch n number of instances on different ports


# t1 = threading.Thread(target=create_instance, args=(5000,))
# t2 = threading.Thread(target=create_instance, args=(5001,))
# t1.start()
# t2.start()

# t1.join()
# t2.join()

