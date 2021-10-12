from socket import *
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

server_address = ('0.0.0.0',9000)

# create the server socket
# TCP socket
server_socket = socket(AF_INET, SOCK_STREAM)

# bind the socket
server_socket.bind(server_address)


server_socket.listen(1)

# accept connection
client_socket, client_address = server_socket.accept() 

# if below code is executed, that means the sender is connected
print(f"[+] {client_address} is connected.")

# receive the file 
filename = client_socket.recv(4096).decode()

# start receive file
with open(filename, "wb") as f:
    while True:
        #read bytes from socket
        file_in = open(filename, "rb")
        private_key = RSA.import_key(open("private.pem").read())
        enc_session_key, nonce, tag, ciphertext = \
            [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        decrypted_data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        data = decrypted_data

        # write to the file the bytes we just received
        f.write(data)

print(f"{filename} Received!")
       

# close the client socket
client_socket.close()
# close the server socket
server_socket.close()