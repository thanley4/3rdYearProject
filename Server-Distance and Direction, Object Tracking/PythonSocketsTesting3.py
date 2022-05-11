import socket

HOST, PORT = "140.203.229.78", 9999

data = "7,-77.000000,1,2,3,4,5,6,7,8,9,10,1.000000,2.000000,3.000000,4.000000,5.000000,6.000000,7.000000,8.000000,9.000000,10.000000,1.000000,2.000000,3.000000,4.000000,5.000000,6.000000,7.000000,8.000000,9.000000,10.000000,1.000000,2.000000,3.000000,4.000000,5.000000,6.000000,7.000000,8.000000,9.000000,10.000000"


def serialize(packet_id, drowsiness, ids, distances, angles, widths):
    return_string = ""
    ids_string = ""
    distances_string = ""
    angles_string = ""
    widths_string = ""
    for i in range(0, len(ids)):
        ids_string = ids_string + "," + ids[i]
        distances_string = distances_string + "," + distances[i]
        angles_string = angles_string + "," + angles[i]
        widths_string = widths_string + "," + widths[i]
    return_string = return_string + packet_id + "," + drowsiness + "," + ids_string + distances_string + angles_string + widths_string
    return return_string


def send_packet(packet_id, drowsiness, ids, distances, angles):
    packet = serialize(packet_id, drowsiness, ids, distances, angles)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(packet + "\n", "utf-8"))
        sock.close()
        print("Sent:     {}".format(packet))

if __name__ == '__main__':
    packet = data

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(packet + "\n", "utf-8"))
        sock.close()
        print("Sent:     {}".format(packet))