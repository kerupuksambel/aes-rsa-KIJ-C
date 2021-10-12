from socket import *
import os
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP

from base64 import b64encode
from time import time

server_address = ('0.0.0.0',9001)

# create the server socket
# TCP socket
server_socket = socket(AF_INET, SOCK_STREAM)

# bind the socket
server_socket.bind(server_address)


server_socket.listen(1)

# accept connection
client_socket, client_address = server_socket.accept() 

print(f"[+] {client_address} is connected.")

# Load RSA priv key 
def recv_rsa(sock):
	private_key = RSA.importKey(open("private.pem").read())
	cipher_rsa = PKCS1_OAEP.new(private_key)
	enc_msg = sock.recv(4096)
	print('New encrypted message : ' + b64encode(enc_msg).decode())

	decrypted_msg = cipher_rsa.decrypt(enc_msg)

	return decrypted_msg

def recv_aes(sock, key, nonce, tag):
	cipher_aes = AES.new(key, AES.MODE_EAX, nonce)
	ciphertext = sock.recv(4096)
	data = cipher_aes.decrypt_and_verify(ciphertext, tag)

	return data

key = recv_rsa(client_socket)
print("base64(key) : " + b64encode(key).decode())
name = recv_rsa(client_socket).decode()
print("Name : " + name)
nonce = recv_rsa(client_socket)
print("base64(nonce) : " + b64encode(nonce).decode())
tag = recv_rsa(client_socket)
print("base64(tag) : " + b64encode(tag).decode())

file = recv_aes(client_socket, key, nonce, tag)
print(f"{name} Received!")

with open('saved/' + name + '_' + str(int(time())), 'wb') as f:
	f.write(file)
       

# close the client socket
client_socket.close()
# close the server socket
server_socket.close()