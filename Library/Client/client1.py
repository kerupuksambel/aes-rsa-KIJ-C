from socket import *
import os, base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

from time import sleep

AES_KEY_SIZE = 16
BLOCK_SIZE = 16

sessionkey = get_random_bytes(AES_KEY_SIZE)

def encrypt(data):
    rsa_key = RSA.importKey(open("receiver.pem").read())
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    
    #Generate a session key randomly

    #Encrypt session key with RSA public key
    enc_sessionkey = cipher_rsa.encrypt(sessionkey)
    cipher_aes = AES.new(sessionkey, AES.MODE_EAX)
    
    #Encrypt data with AES Session Key
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    #Write Encrypted file
    file_out = open("encrypted_data.bin", "wb")
    [ file_out.write(x) for x in (enc_sessionkey, cipher_aes.nonce, tag, ciphertext) ]
    file_out.close()

    # Reread
    res = open("encrypted_data.bin", 'rb').read()

    return res


def send_file(filename, sock):
    #send filename 
    sock.send(f"{filename}".encode())
    
    #send file process
    with open(f"{filename}", "rb") as f:
        while True:
            #read bytes from file
            data = f.read(4096)
            print(data)
            #send all bytes
            sock.sendall(encrypt(data))

    # close the socket
    sock.close()

def send_rsa(msg, sock):
    rsa_key = RSA.importKey(open("receiver.pem").read())
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    enc_msg = cipher_rsa.encrypt(msg)

    print("Encrypted : " + __import__('base64').b64encode(enc_msg).decode())

    sock.send(enc_msg)
    sleep(1)

def send_aes(msg, sock):
    cipher_aes = AES.new(sessionkey, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(msg)

    # Send those values for decryption later
    send_rsa(cipher_aes.nonce, sock)
    send_rsa(tag, sock)

    sock.send(ciphertext)



if __name__ == "__main__":
    argv = __import__('sys').argv
    if(len(argv)) == 1:
        host = input('Masukkan IP address yang ingin dituju : ')
        port = int(input('Masukkan port yang ingin dituju : '))
        filename = input('Masukkan Nama File yang ingin dikirim :')
    else:
        host = 'localhost'
        port = 9001
        filename = 'test.txt'
    file_content = open(filename, 'rb').read()
    
    # connect to socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_address = (host, port)
    client_socket.connect(client_address)
    print("Session Key : " + __import__('base64').b64encode(sessionkey).decode())
    # send key 
    send_rsa(sessionkey, client_socket)
    # send name
    send_rsa(filename.encode(), client_socket)
    # send file
    send_aes(file_content, client_socket)

    client_socket.close()




