import math
import pickle
import socket

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from utils.additional_functions import object_colours, Object, ObjectList

# TCP_IP = '169.254.56.154' # IP When Connecting with Pi
TCP_IP = '127.0.0.1'  # Local IP
TCP_PORT = 5006
BUFFER_SIZE = 20  # Normally 1024, but I want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

# conn, addr = s.accept()


fig = plt.figure(figsize=(16, 9), dpi=120)

ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0.0, 1920), ax.set_xticks([])
ax.set_ylim(1080, 0.0), ax.set_yticks([])

objects_in_frame_list = []

num_objects_in_frame = 50

objects_in_frame = np.zeros(num_objects_in_frame, dtype=[('position', float, (2,)),
                                                         ('size', float),
                                                         ('in_frame', bool),
                                                         ('color', float, (3,))])

objects_in_frame['position'][:, 0] = -1000
objects_in_frame['position'][:, 1] = -1000
objects_in_frame['size'] = 10
objects_in_frame['in_frame'] = False
objects_in_frame['color'] = [1, 0, 0]

scatter_plot = ax.scatter(objects_in_frame['position'][:, 0], objects_in_frame['position'][:, 1],
                          s=objects_in_frame['size'], edgecolors=objects_in_frame['color'],
                          facecolors=objects_in_frame['color'])

field_of_view = ax.plot([417, 960, 1503], [0, 900, 0], color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

ten_meter_arc = ax.plot(
    [908.35, 917.74, 925.80, 934.12, 942.64, 951.28, 960.00, 968.72, 977.36, 985.88, 994.20, 1002.26, 1011.65],
    [814.37, 809.37, 806.03, 803.41, 801.52, 800.38, 800.00, 800.38, 801.52, 803.41, 806.03, 809.37, 814.37],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

twenty_meter_arc = ax.plot(
    [856.69, 875.48, 891.60, 908.24, 925.27, 942.57, 960.00, 977.43, 994.73, 1011.76, 1028.40, 1044.52, 1063.31],
    [728.75, 718.74, 712.06, 706.81, 703.04, 700.76, 700.00, 700.76, 703.04, 706.81, 712.06, 718.74, 728.75],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

thirty_meter_arc = ax.plot(
    [805.04, 833.21, 857.39, 882.35, 907.91, 933.85, 960.00, 986.15, 1012.09, 1037.65, 1062.61, 1086.79, 1114.96],
    [643.12, 628.11, 618.09, 610.22, 604.56, 601.14, 600.00, 601.14, 604.56, 610.22, 618.09, 628.11, 643.12],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

forty_meter_arc = ax.plot(
    [753.39, 790.95, 823.19, 856.47, 890.54, 925.14, 960.00, 994.86, 1029.46, 1063.53, 1096.81, 1129.05, 1166.61],
    [557.49, 537.48, 524.12, 513.63, 506.08, 501.52, 500.00, 501.52, 506.08, 513.63, 524.12, 537.48, 557.49],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

fifty_meter_arc = ax.plot(
    [701.73, 748.69, 788.99, 830.59, 873.18, 916.42, 960.00, 1003.58, 1046.82, 1089.41, 1131.01, 1171.31, 1218.27],
    [471.87, 446.85, 430.15, 417.04, 407.60, 401.90, 400.00, 401.90, 407.60, 417.04, 430.15, 446.85, 471.87],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

sixty_meter_arc = ax.plot(
    [650.08, 706.43, 754.79, 804.71, 855.81, 907.71, 960.00, 1012.29, 1064.19, 1115.29, 1165.21, 1213.57, 1269.92],
    [386.24, 356.22, 336.18, 320.44, 309.12, 302.28, 300.00, 302.28, 309.12, 320.44, 336.18, 356.22, 386.24],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

seventy_meter_arc = ax.plot(
    [598.43, 664.17, 720.59, 778.83, 838.45, 898.99, 960.00, 1021.01, 1081.55, 1141.17, 1199.41, 1255.83, 1321.57],
    [300.61, 265.58, 242.22, 223.85, 210.63, 202.66, 200.00, 202.66, 210.63, 223.85, 242.22, 265.58, 300.61],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

eighty_meter_arc = ax.plot(
    [546.77, 621.91, 686.38, 752.94, 821.08, 890.28, 960.00, 1029.72, 1098.92, 1167.06, 1233.62, 1298.09, 1373.23],
    [214.99, 174.95, 148.25, 127.26, 112.15, 103.04, 100.00, 103.04, 112.15, 127.26, 148.25, 174.95, 214.99],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

ninety_meter_arc = ax.plot(
    [495.12, 579.64, 652.18, 727.06, 803.72, 881.56, 960.00, 1038.44, 1116.28, 1192.94, 1267.82, 1340.36, 1424.88],
    [129.36, 84.32, 54.28, 30.67, 13.67, 3.42, 0.00, 3.42, 13.67, 30.67, 54.28, 84.32, 129.36],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

hundred_meter_arc = ax.plot(
    [443.47, 537.38, 617.98, 701.18, 786.35, 872.84, 960.00, 1047.16, 1133.65, 1218.82, 1302.02, 1382.62, 1476.53],
    [43.73, -6.31, -39.69, -65.93, -84.81, -96.19, -100.00, -96.19, -84.81, -65.93, -39.69, -6.31, 43.73],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

left_fill = ax.fill((0, 0, 1920, 1920, 1503, 960, 417), (0, 1080, 1080, 0, 0, 900, 0), color=(0.8, 0.8, 0.8, 0.8))


def check_for_update():
    conn, addr = s.accept()
    data = []
    while True:
        packet = conn.recv(BUFFER_SIZE)
        if not packet:
            break
        data.append(packet)
    data_arr = pickle.loads(b"".join(data))
    print("Object Recieved:")
    print(data_arr)
    conn.close()
    return data_arr


def update(frame_number):
    current_index = frame_number % num_objects_in_frame

    object_list = check_for_update()

    print("List of Objects in Frame: ")

    objects_in_frame['position'][:, 0] = -1000
    objects_in_frame['position'][:, 1] = -1000
    objects_in_frame['size'] = 10
    objects_in_frame['in_frame'] = False

    for i in range(0, len(object_list.list_of_objects)):
        print(i)
        # X - Position
        # objects_in_frame['position'][:, 0] = np.random.uniform(0, 1920, num_objects_in_frame)
        objects_in_frame['position'][i, 0] = round(960 + object_list.list_of_objects[i].distance * 10 * math.sin(
            math.radians(object_list.list_of_objects[i].angle)))

        # Y - Position
        # objects_in_frame['position'][:, 1] = np.random.uniform(0, 1080, num_objects_in_frame)
        objects_in_frame['position'][i, 1] = round(900 - object_list.list_of_objects[i].distance * 10 * math.cos(
            math.radians(object_list.list_of_objects[i].angle)))

        # Size - Diameter * Unknown
        objects_in_frame['size'][i] = (((object_list.list_of_objects[i].width * 10) - 5) * 3 / 5) ** 2

        # Colour
        objects_in_frame['color'][i] = object_colours[object_list.list_of_objects[i].object_id]

    # Update Scatter Plot Positions
    scatter_plot.set_offsets(objects_in_frame['position'])

    # Update Scatter Plot Sizes
    scatter_plot.set_sizes(objects_in_frame['size'])

    # Update Scatter Plot Colours
    scatter_plot.set_facecolors(objects_in_frame['color'])
    scatter_plot.set_edgecolors(objects_in_frame['color'])


animation = FuncAnimation(fig, update, interval=33)
plt.show()
