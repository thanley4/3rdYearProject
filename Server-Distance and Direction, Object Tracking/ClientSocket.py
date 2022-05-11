import socket
import pickle
import time

TCP_IP = '169.254.56.154'
TCP_PORT = 5005
BUFFER_SIZE = 1024

cars = ["Ford", "Volvo", "BMW"]

for i in range(0, 10000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    print("Sending Packet ", i)
    time.sleep(0.1)
    s.send((pickle.dumps(cars)))
    s.close()