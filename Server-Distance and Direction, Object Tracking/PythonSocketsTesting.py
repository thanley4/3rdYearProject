import random
import socket
import pickle
import math

# TCP_IP = '169.254.56.154'
import time

TCP_IP = '192.168.1.8'  # Local IP
TCP_PORT = 5005
BUFFER_SIZE = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while (True):
    print("Sending Packet ")
    s.send(str.encode("77,-77.000000,1,2,3,4,5,6,7,8,9,10,1.000000,2.000000,3.000000,4.000000,5.000000,6.000000,7.000000,8.000000,9.000000,10.000000,1.000000,2.000000,3.000000,4.000000,5.000000,6.000000,7.000000,8.000000,9.000000,10.000000"))
    time.sleep(1000 + random.randint(1, 1000))

    packet = s.recv(BUFFER_SIZE)
    print(packet)
