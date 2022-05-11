import socketserver


def deserialize(received_string):
    delimited = received_string.split(",")
    packet_id = int(delimited[0])
    drowsiness = float(delimited[1])
    ids = []
    distances = []
    angles = []
    widths = []
    num_objects = int((len(delimited) - 2) / 4)
    print("Num Objects: ", num_objects)

    for i in range(2, num_objects + 2, 1):
        ids.append(delimited[i])

    for i in range(2 + num_objects, (2 * num_objects) + 2, 1):
        distances.append(delimited[i])

    for i in range(2 + (2 * num_objects), (3 * num_objects) + 2, 1):
        angles.append(delimited[i])

    for i in range(2 + (3 * num_objects), (4 * num_objects) + 2, 1):
        widths.append(delimited[i])

    return packet_id, drowsiness, ids, distances, angles, widths


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(2048).strip()
        print("Raw Data: ", self.data)
        print("Decoded Data: ", self.data.decode())
        packet_id, drowsiness, ids, distances, angles, widths = deserialize(self.data.decode())
        print("packetID: ", str(packet_id), "\ndrowsyness: ", str(drowsiness), "\nIDs: ", str(ids), "\ndistances: ",
              str(distances), "\nangles: ", str(angles), "\nwidths: ", str(widths))
        # update frame function call here


if __name__ == "__main__":
    HOST, PORT = "169.254.56.154", 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
        print("testing if continue")
