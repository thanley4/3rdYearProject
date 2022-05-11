import math
import socket
import socketserver
import matplotlib.pyplot as plt
import numpy as np
import threading

from matplotlib.animation import FuncAnimation
from utils.additional_functionsV3 import object_colours, deserialize
from ObjectTrackingV6 import assign_objects

objects_in_frame_list = []

max_objects_in_frame = 50
num_objects_in_frame = max_objects_in_frame

packet_id = 0
drowsiness = 0.0
ids = []
distances = []
angles = []
widths = []
objects_in_frame = np.zeros(max_objects_in_frame, dtype=[('position (t+1)', float, (2,)),
                                                         ('position (t)', float, (2,)),
                                                         ('position (t-1)', float, (2,)),
                                                         ('position (t-2)', float, (2,)),
                                                         ('position (t-3)', float, (2,)),
                                                         ('position (t-4)', float, (2,)),
                                                         ('position (t-5)', float, (2,)),
                                                         ('position (t-6)', float, (2,)),
                                                         ('velocity (t)', float, (2,)),
                                                         ('velocity (t-1)', float, (2,)),
                                                         ('velocity (t-2)', float, (2,)),
                                                         ('id', int),
                                                         ('size', float),
                                                         ('color', float, (3,)),
                                                         ('match', bool)])


class MyDataClass:

    def __init__(self):
        self.objects_in_frame = objects_in_frame

        self.objects_in_frame['position (t+1)'][:, 0] = -1000
        self.objects_in_frame['position (t+1)'][:, 1] = -1000
        self.objects_in_frame['position (t)'][:, 0] = -1000
        self.objects_in_frame['position (t)'][:, 1] = -1000
        self.objects_in_frame['position (t-1)'][:, 0] = -1000
        self.objects_in_frame['position (t-1)'][:, 1] = -1000
        self.objects_in_frame['position (t-2)'][:, 0] = -1000
        self.objects_in_frame['position (t-2)'][:, 1] = -1000
        self.objects_in_frame['position (t-3)'][:, 0] = -1000
        self.objects_in_frame['position (t-3)'][:, 1] = -1000
        self.objects_in_frame['position (t-4)'][:, 0] = -1000
        self.objects_in_frame['position (t-4)'][:, 1] = -1000
        self.objects_in_frame['position (t-5)'][:, 0] = -1000
        self.objects_in_frame['position (t-5)'][:, 1] = -1000
        self.objects_in_frame['position (t-6)'][:, 0] = -1000
        self.objects_in_frame['position (t-6)'][:, 1] = -1000
        self.objects_in_frame['velocity (t)'][:, 0] = 10
        self.objects_in_frame['velocity (t)'][:, 1] = 10
        self.objects_in_frame['velocity (t-1)'][:, 0] = 0
        self.objects_in_frame['velocity (t-1)'][:, 1] = 0
        self.objects_in_frame['velocity (t-2)'][:, 0] = 0
        self.objects_in_frame['velocity (t-2)'][:, 1] = 0
        self.objects_in_frame['id'] = 999
        self.objects_in_frame['size'] = 10
        self.objects_in_frame['color'] = [1, 0, 0]
        self.objects_in_frame['match'] = False


class MyPlotClass():

    def __init__(self, dataClass):
        self._dataClass = dataClass

        x = 1920
        y = x / 16 * 9

        fig = plt.figure(figsize=(16, 9), dpi=(x / 16))
        ax = fig.add_axes([0, 0, 1, 1], frameon=False)
        ax.set_xlim(0.0, x), ax.set_xticks([])
        ax.set_ylim(y, 0.0), ax.set_yticks([])

        self.scatter_plot = ax.scatter(self._dataClass.objects_in_frame['position (t)'][:, 0],
                                       self._dataClass.objects_in_frame['position (t)'][:, 1],
                                       s=self._dataClass.objects_in_frame['size'],
                                       edgecolors=[0, 0, 0],
                                       facecolors=self._dataClass.objects_in_frame['color'])

        self.scatter_plot_1 = ax.scatter(self._dataClass.objects_in_frame['position (t-1)'][:, 0],
                                         self._dataClass.objects_in_frame['position (t-1)'][:, 1],
                                         s=10, edgecolors=[0, 1, 1], facecolors="None")

        self.scatter_plot_2 = ax.scatter(self._dataClass.objects_in_frame['position (t-2)'][:, 0],
                                         self._dataClass.objects_in_frame['position (t-2)'][:, 1],
                                         s=10, edgecolors=[0, 1, 1], facecolors="None")

        self.scatter_plot_3 = ax.scatter(self._dataClass.objects_in_frame['position (t-3)'][:, 0],
                                         self._dataClass.objects_in_frame['position (t-3)'][:, 1],
                                         s=10, edgecolors=[0, 1, 1], facecolors="None")

        self.scatter_plot_4 = ax.scatter(self._dataClass.objects_in_frame['position (t-4)'][:, 0],
                                         self._dataClass.objects_in_frame['position (t-4)'][:, 1],
                                         s=10, edgecolors=[0, 1, 1], facecolors="None")

        self.scatter_plot_5 = ax.scatter(self._dataClass.objects_in_frame['position (t-5)'][:, 0],
                                         self._dataClass.objects_in_frame['position (t-5)'][:, 1],
                                         s=10, edgecolors=[0, 1, 1], facecolors="None")

        self.scatter_plot_6 = ax.scatter(self._dataClass.objects_in_frame['position (t-6)'][:, 0],
                                         self._dataClass.objects_in_frame['position (t-6)'][:, 1],
                                         s=10, edgecolors=[0, 1, 1], facecolors="None")

        # Decorative Graphics

        field_of_view = ax.plot([417, 960, 1503], [0, 900, 0], color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

        ten_meter_arc = ax.plot(
            [856.69, 875.48, 891.60, 908.24, 925.27, 942.57, 960.00, 977.43, 994.73, 1011.76, 1028.40, 1044.52,
             1063.31],
            [728.75, 718.74, 712.06, 706.81, 703.04, 700.76, 700.00, 700.76, 703.04, 706.81, 712.06, 718.74, 728.75],
            color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

        twenty_meter_arc = ax.plot(
            [753.39, 790.95, 823.19, 856.47, 890.54, 925.14, 960.00, 994.86, 1029.46, 1063.53, 1096.81, 1129.05,
             1166.61],
            [557.49, 537.48, 524.12, 513.63, 506.08, 501.52, 500.00, 501.52, 506.08, 513.63, 524.12, 537.48, 557.49],
            color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

        thirty_meter_arc = ax.plot(
            [650.08, 706.43, 754.79, 804.71, 855.81, 907.71, 960.00, 1012.29, 1064.19, 1115.29, 1165.21, 1213.57,
             1269.92],
            [386.24, 356.22, 336.18, 320.44, 309.12, 302.28, 300.00, 302.28, 309.12, 320.44, 336.18, 356.22, 386.24],
            color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

        forty_meter_arc = ax.plot(
            [546.77, 621.91, 686.38, 752.94, 821.08, 890.28, 960.00, 1029.72, 1098.92, 1167.06, 1233.62, 1298.09,
             1373.23],
            [214.99, 174.95, 148.25, 127.26, 112.15, 103.04, 100.00, 103.04, 112.15, 127.26, 148.25, 174.95, 214.99],
            color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

        fifty_meter_arc = ax.plot(
            [443.47, 537.38, 617.98, 701.18, 786.35, 872.84, 960.00, 1047.16, 1133.65, 1218.82, 1302.02, 1382.62,
             1476.53],
            [43.73, -6.31, -39.69, -65.93, -84.81, -96.19, -100.00, -96.19, -84.81, -65.93, -39.69, -6.31, 43.73],
            color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

        shading = ax.fill((0, 0, 1920, 1920, 1503, 960, 417), (0, 1080, 1080, 0, 0, 900, 0), color=(0.8, 0.8, 0.8, 0.8))

        car = ax.fill((944, 976, 976, 944), (884, 884, 964, 964), color=(0, 0, 1, 1))

        self.ani = FuncAnimation(fig, self.update, repeat=True)

    def update(self, i):
        print("UPDATE", i)

        self._dataClass.objects_in_frame['color'] = object_colours[0]

        # Update Scatter Plot Positions
        self.scatter_plot.set_offsets(self._dataClass.objects_in_frame['position (t)'])
        self.scatter_plot_1.set_offsets(self._dataClass.objects_in_frame['position (t-1)'])
        self.scatter_plot_2.set_offsets(self._dataClass.objects_in_frame['position (t-2)'])
        self.scatter_plot_3.set_offsets(self._dataClass.objects_in_frame['position (t-3)'])
        self.scatter_plot_4.set_offsets(self._dataClass.objects_in_frame['position (t-4)'])
        self.scatter_plot_5.set_offsets(self._dataClass.objects_in_frame['position (t-5)'])
        self.scatter_plot_6.set_offsets(self._dataClass.objects_in_frame['position (t-6)'])

        # Update Scatter Plot Sizes
        self.scatter_plot.set_sizes(self._dataClass.objects_in_frame['size'])

        # Update Scatter Plot Colours
        self.scatter_plot.set_facecolors(self._dataClass.objects_in_frame['color'])
        # self.scatter_plot.set_edgecolors(self._dataClass.objects_in_frame['color'])


class MyTCPHandler(socketserver.BaseRequestHandler):
    global num_objects_in_frame, objects_in_frame

    def handle(self):
        self.data = self.request.recv(2048).strip()
        global num_objects_in_frame, objects_in_frame
        print(self.data.decode())
        packet_id, drowsiness, ids, distances, angles, widths = deserialize(self.data.decode())
        num_new_objects = len(ids)
        print("New Packet with", num_new_objects, "objects")
        # print("packetID: ", str(packet_id), "\ndrowsyness: ", str(drowsiness), "\nIDs: ", str(ids), "\ndistances: ",
        #       str(distances), "\nangles: ", str(angles), "\nwidths: ", str(widths))

        new_frame = np.zeros(num_new_objects, dtype=[('position (t)', float, (2,)),
                                                     ('id', int),
                                                     ('size', float),
                                                     ('match', bool)])

        for i in range(0, num_new_objects):
            new_frame['position (t)'][i, 0] = round(960 + distances[i] * 20 * math.sin(
                math.radians(angles[i])))

            new_frame['position (t)'][i, 1] = round(900 - distances[i] * 20 * math.cos(
                math.radians(angles[i])))

            new_frame['id'][i] = ids[i]

            new_frame['size'][i] = (((widths[i] * 20) - 5) * 3 / 5) ** 2

        objects_in_frame, num_objects_in_frame = assign_objects(objects_in_frame, num_objects_in_frame, new_frame,
                                                                num_new_objects, 1 / 30.5, 13.88)


class MyDataFetchClass(threading.Thread):

    def __init__(self, dataClass):
        threading.Thread.__init__(self)

        self._dataClass = dataClass

    def run(self):
        HOST, PORT = "140.203.229.78", 9999

        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
            server.serve_forever()


data = MyDataClass()
plotter = MyPlotClass(data)
fetcher = MyDataFetchClass(data)

fetcher.start()
plt.show()
# fetcher.join()
