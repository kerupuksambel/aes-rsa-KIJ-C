from socket import *
import os

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
        data = client_socket.recv(4096).decode()

        # write to the file the bytes we just received
        f.write(data)

print(f"{filename} Received!")
       

# close the client socket
client_socket.close()
# close the server socket
server_socket.close()