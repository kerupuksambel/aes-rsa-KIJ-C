from socket import *
from base64 import *

from AES import enc, dec
from RSA import enc, dec

server_address = ('localhost', 5000)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(1)
client_socket, client_address = server_socket.accept()

# First, receive the keys 
data = client_socket.recv(1024*32).decode()
keys = (eval(b64encode(data)))

# Second, use the keys for AES decryption
 

client_socket.close()
server_socket.close()