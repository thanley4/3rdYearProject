import socket
import struct

PORT, HOST_IP = 5005, '140.203.224.191'
key = 4

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST_IP, PORT))
    s.listen()
    print("starting to listen")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            # t = (input("Input: "))
            t = "testing"
            u = str.encode(t)
            print(u)

            # assert t >= 0
            d = struct.pack('s', u)
            conn.sendall(d)

            packet = conn.recv(2048)
            print(packet)