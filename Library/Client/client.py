from socket import *
import os
from cryptography.fernet import Fernet

def encrypt(filename):
    file = open('key.key','rb')
    key = file.read()
    file.close()

    with open(filename,'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(f"{filename}.encrypted",'wb') as f:
        f.write(encrypted)

    encrypted_file = (f"{filename}.encrypted")
    return encrypted_file

def send_file(encrypted_file,host,port):
    #connect to socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_address = (host, port)
    client_socket.connect(client_address)

    #send filename 
    client_socket.send(f"{encrypted_file}".encode())
    
    #send file process
    with open(encrypted_file, "rb") as f:
        while True:
            #read bytes from file
            data = f.read(4096)
            
            #send all bytes
            client_socket.sendall(data)

    # close the socket
    client_socket.close()

if __name__ == "__main__":
    host = input('Masukkan IP address yang ingin dituju : ')
    port = int(input('Masukkan port yang ingin dituju : '))
    filename = input('Masukkan Nama File yang ingin dikirim :')
    encrypted_file = encrypt(filename)
    send_file(encrypted_file,host,port)




