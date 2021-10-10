from socket import *
from base64 import *

import AES, RSA

server_address = ('localhost', 5000)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(1)
client_socket, client_address = server_socket.accept()

# First, receive the keys 
data = client_socket.recv(1024).decode()
enc_keys = b64decode(data)
try:
    keys = int(enc_keys.decode())
except:
    print('Invalid RSA key.')
    client_socket.close()
keys = RSA.dec(keys).decode()

print(keys)

# Second, use the keys for AES decryption


client_socket.close()
server_socket.close()