from socket import *
from base64 import *

from AES import enc, dec, keys
from RSA import enc as encRSA

ip = input('Masukkan IP address yang ingin dituju : ')
port = int(input('Masukkan port yang ingin dituju : '))

server_address = (ip, port)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(server_address)

print("Terhubung ke {}:{}".format(ip, str(port)))

# First, send the key with RSA.
b64key = b64encode(str(keys))
client_socket.send(b64key.encode())

path = input('File : ')
try:
    with open(path, 'rb') as f:
        b64f = b64encode(f.read())
except Exception as e:
    print('Error : File tidak bisa dibuka.')
    exit()
    
# AES implementation : File in base64 encrypted with AES

client_socket.send(b64f.encode())
data = client_socket.recv(1024).decode()

print(data)

client_socket.close()