import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 4444))#(IP, Port), need to change IP after testing when not on same PC

s.send(bytes("Hello", "utf-8"))
msg = s.recv(1024)#max size of message

print(msg.decode("utf-8"))
