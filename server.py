import socket
import pickle


# IP Laptop: '192.168.0.108'
# IP PC: '192.168.0.110'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 4444))#(IP, Port)
s.listen(5) #queue size
print(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))
while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established")

    data = clientsocket.recv(1024)
    msg = pickle.loads(data)
    print(msg)

    clientsocket.send(bytes("Welcome to the server!", "utf-8"))#send data to clientsocket
    clientsocket.close()




