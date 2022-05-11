import socket
import pickle
import time

TCP_IP = '169.254.56.154'  # this IP of my pc. When I want raspberry pi 2`s as a server, I replace it with its IP '169.254.54.195'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but I want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
# print ('Connection address:', addr)
# while 1:
#     data = conn.recv(BUFFER_SIZE)
#     if not data: break
#     print ("received data:", pickle.loads(data))
#     conn.send(data)  # echo
# conn.close()

data = []
while True:
    packet = conn.recv(BUFFER_SIZE)
    if not packet: break
    data.append(packet)
data_arr = pickle.loads(b"".join(data))
print(data_arr)
conn.close()

conn, addr = s.accept()
data = []
while True:
    packet = conn.recv(BUFFER_SIZE)
    if not packet: break
    data.append(packet)
data_arr = pickle.loads(b"".join(data))
print(data_arr)
conn.close()