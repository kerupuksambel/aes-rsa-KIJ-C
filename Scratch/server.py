from socket import *
from base64 import *
from time import time

import AES, RSA

server_address = ('localhost', 5001)

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
    print('Invalid RSA cipher.')
    client_socket.close()
keys = RSA.dec(keys).decode()

print('Key received : ' + keys)

# Second, receive the name
data = client_socket.recv(1024).decode()
enc_name = b64decode(data)
print(enc_name)
try:
    name = int(enc_name.decode())
except:
    print('Invalid RSA cipher.')
    client_socket.close()
name = RSA.dec(name).decode()

print('Filename : ' + name)

# Third, use the keys for AES decryption
data = client_socket.recv(1024).decode()
data = data.split('|')
file_content = b''
for d in data:
    decoded = b64decode(d)
    print(len(decoded))
    print(keys)
    decrypted = AES.dec(decoded, keys.encode())
    cont = ''.join([chr(_) for _ in decrypted]).encode()
    file_content += cont

print(file_content)
file_content = file_content.rstrip(b'\x00')   

# Finally, save the file with received name
with open('saved/' + name + '_' + str(int(time())), 'wb') as f:
    f.write(file_content)

client_socket.close()
server_socket.close()