import socket


def deserialize(received_string):
    delimited = received_string.split(",")
    packet_id = int(delimited[0])
    drowsiness = float(delimited[1])
    ids = []
    distances = []
    angles = []
    num_objects = int((len(delimited) - 2) / 3)
    print("Num Objects: ", num_objects)

    for i in range(2, num_objects + 2, 1):
        ids.append(delimited[i])

    for i in range(2 + num_objects, (2 * num_objects) + 2, 1):
        distances.append(delimited[i])

    for i in range(2 + (2 * num_objects), (3 * num_objects) + 2, 1):
        angles.append(delimited[i])

    return packet_id, drowsiness, ids, distances, angles


TCP_IP = '140.203.224.215'
TCP_PORT = 5005
BUFFER_SIZE = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind((TCP_IP, 5006))
s2.listen(1)

conn, addr = s.accept()

conn, addr = s2.accept()



while True:
    packet = conn.recv(BUFFER_SIZE)
    packet_id, drowsiness, ids, distances, angles = deserialize(packet.decode())

    print("packetID: ", str(packet_id), "\ndrowsyness: ", str(drowsiness), "\nIDs: ", str(ids), "\ndistances: ", str(distances), "\nangles: ", str(angles))

    send = str.encode("Hello from Server: ")
    conn.send(send)
    # print("Packet Sent:", send)

conn.close()
