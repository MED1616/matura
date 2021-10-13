import socket
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 4444))#(IP, Port)
s.listen(5) #queue size
print(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))
while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established")

    data = clientsocket.recv(1024)
    data = data.decode("utf-8")
    print(data)
    clientsocket.send(bytes("Welcome to the server!", "utf-8"))#send data to clientsocket
    clientsocket.close()