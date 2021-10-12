from socket import *
import os, base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

AES_KEY_SIZE = 16
BLOCK_SIZE = 16


def encrypt(filename):
    rsa_key = RSA.import_key(open("receiver.pem").read())
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    
    with open(filename,'rb') as f:
        data = f.read()
    #Generate a session key randomly
    sessionkey = get_random_bytes(AES_KEY_SIZE)

    #Encrypt session key with RSA public key
    enc_sessionkey = cipher_rsa.encrypt(sessionkey)
    cipher_aes = AES.new(sessionkey, AES.MODE_EAX)
    
    #Encrypt data with AES Session Key
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    #Write Encrypted file
    file_out = open("encrypted_data.bin", "wb")
    [ file_out.write(x) for x in (enc_sessionkey, cipher_aes.nonce, tag, ciphertext) ]
    file_out.close()
        
    return file_out


def send_file(filename,host,port):
    #connect to socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_address = (host, port)
    client_socket.connect(client_address)

    #send filename 
    client_socket.send(f"{filename}".encode())
    
    #send file process
    with open(f"{filename}", "rb") as f:
        while True:
            #read bytes from file
            data = f.read(4096)
            print(data)
            #send all bytes
            client_socket.sendall(encrypt(data))

    # close the socket
    client_socket.close()

if __name__ == "__main__":
    host = input('Masukkan IP address yang ingin dituju : ')
    port = int(input('Masukkan port yang ingin dituju : '))
    filename = input('Masukkan Nama File yang ingin dikirim :')
    # encrypt_file = encrypt(filename)
    send_file(filename,host,port)




