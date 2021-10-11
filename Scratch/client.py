from socket import *
from base64 import *
from os.path import basename

import RSA, AES

from sys import argv

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if(len(argv) == 1):
    ip = input('IP address : ')
    port = int(input('Port : '))
elif argv[1] == 'debug':
    ip = 'localhost'
    port = 5001

server_address = (ip, port)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(server_address)

print("Connected to {}:{}".format(ip, str(port)))

# First, send the key with RSA.
orig_key = AES.keys
key = RSA.enc(orig_key.decode())
key = b64encode(str(key).encode()).decode()
client_socket.send(key.encode())

if(len(argv) == 1):
    path = input('File : ')
elif argv[1] == 'debug':
    path = 'ContohFile'

filename = basename(path)
filename = RSA.enc(filename)
filename = b64encode(str(filename).encode()).decode()
client_socket.send(filename.encode())

try:
    with open(path, 'rb') as f:
        # Generate chunks of files
        fchunks = chunks(f.read(), 1024)

except Exception as e:
    print('Error : File tidak bisa dibuka.')
    exit()
    
# AES implementation : File in base64 encrypted with AES
## For every chunks, split it into 16 bytes. If there's some remaining, fill with null bytes
for fc in fchunks:
    fc += b'\x00' * (16 - len(fc) % 16)
    ch = chunks(fc, 16)
    payload = []
    for c in ch:
        enc_chunk = AES.enc(c, orig_key)
        payload.append(b64encode(bytes(enc_chunk)))
    payload = '|'.join(_.decode() for _ in payload)
    print(payload)
    client_socket.send(payload.encode())

data = client_socket.recv(1024).decode()

client_socket.close()