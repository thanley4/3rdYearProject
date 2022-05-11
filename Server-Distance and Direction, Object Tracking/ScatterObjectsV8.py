import math
import pickle
import socket
from random import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from numpy import ndarray

from utils.additional_functions import object_colours
from ObjectTrackingV4 import assign_objects

# Sockets Variables
# TCP_IP = '169.254.56.154' # IP When Connecting with Pi
TCP_IP = '127.0.0.1'  # Local IP
TCP_PORT = 5006
BUFFER_SIZE = 20  # Normally 1024, but I want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

# Matplotlib Variables
x = 1920
y = x / 16 * 9

fig = plt.figure(figsize=(16, 9), dpi=(x / 16))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0.0, x), ax.set_xticks([])
ax.set_ylim(y, 0.0), ax.set_yticks([])

objects_in_frame_list = []

num_objects_in_frame = 50

objects_in_frame = np.zeros(num_objects_in_frame, dtype=[('position (t+1)', float, (2,)),
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

objects_in_frame['position (t+1)'][:, 0] = -1000
objects_in_frame['position (t+1)'][:, 1] = -1000
objects_in_frame['position (t)'][:, 0] = -1000
objects_in_frame['position (t)'][:, 1] = -1000
objects_in_frame['position (t-1)'][:, 0] = -1000
objects_in_frame['position (t-1)'][:, 1] = -1000
objects_in_frame['position (t-2)'][:, 0] = -1000
objects_in_frame['position (t-2)'][:, 1] = -1000
objects_in_frame['position (t-3)'][:, 0] = -1000
objects_in_frame['position (t-3)'][:, 1] = -1000
objects_in_frame['position (t-4)'][:, 0] = -1000
objects_in_frame['position (t-4)'][:, 1] = -1000
objects_in_frame['position (t-5)'][:, 0] = -1000
objects_in_frame['position (t-5)'][:, 1] = -1000
objects_in_frame['position (t-6)'][:, 0] = -1000
objects_in_frame['position (t-6)'][:, 1] = -1000
objects_in_frame['velocity (t)'][:, 0] = 10
objects_in_frame['velocity (t)'][:, 1] = 10
objects_in_frame['velocity (t-1)'][:, 0] = 0
objects_in_frame['velocity (t-1)'][:, 1] = 0
objects_in_frame['velocity (t-2)'][:, 0] = 0
objects_in_frame['velocity (t-2)'][:, 1] = 0
objects_in_frame['id'] = 999
objects_in_frame['size'] = 10
objects_in_frame['color'] = [1, 0, 0]
objects_in_frame['match'] = False

scatter_plot = ax.scatter(objects_in_frame['position (t)'][:, 0], objects_in_frame['position (t)'][:, 1],
                          s=objects_in_frame['size'], edgecolors=objects_in_frame['color'],
                          facecolors=objects_in_frame['color'])

scatter_plot_1 = ax.scatter(objects_in_frame['position (t-1)'][:, 0], objects_in_frame['position (t-1)'][:, 1],
                            s=10, edgecolors=[0, 1, 1], facecolors="None")

scatter_plot_2 = ax.scatter(objects_in_frame['position (t-2)'][:, 0], objects_in_frame['position (t-2)'][:, 1],
                            s=10, edgecolors=[0, 1, 1], facecolors="None")

scatter_plot_3 = ax.scatter(objects_in_frame['position (t-3)'][:, 0], objects_in_frame['position (t-3)'][:, 1],
                            s=10, edgecolors=[0, 1, 1], facecolors="None")

scatter_plot_4 = ax.scatter(objects_in_frame['position (t-4)'][:, 0], objects_in_frame['position (t-4)'][:, 1],
                            s=10, edgecolors=[0, 1, 1], facecolors="None")

scatter_plot_5 = ax.scatter(objects_in_frame['position (t-5)'][:, 0], objects_in_frame['position (t-5)'][:, 1],
                            s=10, edgecolors=[0, 1, 1], facecolors="None")

scatter_plot_6 = ax.scatter(objects_in_frame['position (t-6)'][:, 0], objects_in_frame['position (t-6)'][:, 1],
                            s=10, edgecolors=[0, 1, 1], facecolors="None")

# Decorative Graphics

field_of_view = ax.plot([417, 960, 1503], [0, 900, 0], color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

ten_meter_arc = ax.plot(
    [856.69, 875.48, 891.60, 908.24, 925.27, 942.57, 960.00, 977.43, 994.73, 1011.76, 1028.40, 1044.52, 1063.31],
    [728.75, 718.74, 712.06, 706.81, 703.04, 700.76, 700.00, 700.76, 703.04, 706.81, 712.06, 718.74, 728.75],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

twenty_meter_arc = ax.plot(
    [753.39, 790.95, 823.19, 856.47, 890.54, 925.14, 960.00, 994.86, 1029.46, 1063.53, 1096.81, 1129.05, 1166.61],
    [557.49, 537.48, 524.12, 513.63, 506.08, 501.52, 500.00, 501.52, 506.08, 513.63, 524.12, 537.48, 557.49],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

thirty_meter_arc = ax.plot(
    [650.08, 706.43, 754.79, 804.71, 855.81, 907.71, 960.00, 1012.29, 1064.19, 1115.29, 1165.21, 1213.57, 1269.92],
    [386.24, 356.22, 336.18, 320.44, 309.12, 302.28, 300.00, 302.28, 309.12, 320.44, 336.18, 356.22, 386.24],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

forty_meter_arc = ax.plot(
    [546.77, 621.91, 686.38, 752.94, 821.08, 890.28, 960.00, 1029.72, 1098.92, 1167.06, 1233.62, 1298.09, 1373.23],
    [214.99, 174.95, 148.25, 127.26, 112.15, 103.04, 100.00, 103.04, 112.15, 127.26, 148.25, 174.95, 214.99],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

fifty_meter_arc = ax.plot(
    [443.47, 537.38, 617.98, 701.18, 786.35, 872.84, 960.00, 1047.16, 1133.65, 1218.82, 1302.02, 1382.62, 1476.53],
    [43.73, -6.31, -39.69, -65.93, -84.81, -96.19, -100.00, -96.19, -84.81, -65.93, -39.69, -6.31, 43.73],
    color=(0.8, 0.8, 0.8, 0.8), linestyle=":")

shading = ax.fill((0, 0, 1920, 1920, 1503, 960, 417), (0, 1080, 1080, 0, 0, 900, 0), color=(0.8, 0.8, 0.8, 0.8))


def check_for_update():
    conn, addr = s.accept()
    data = []
    while True:
        packet = conn.recv(BUFFER_SIZE)
        if not packet:
            break
        data.append(packet)
    data_arr = pickle.loads(b"".join(data))
    # print("Object Recieved:")
    # print(data_arr)
    conn.close()
    return data_arr


def update(frame_number):
    drowsiness = 0.7
    flash_on = False
    frame_number = frame_number + 1
    global objects_in_frame

    object_list = check_for_update()

    new_frame = np.zeros(len(object_list.list_of_objects), dtype=[('position (t)', float, (2,)),
                                                                  ('id', int),
                                                                  ('size', float),
                                                                  ('match', bool)])

    for i in range(0, len(object_list.list_of_objects)):
        new_frame['position (t)'][i, 0] = round(960 + object_list.list_of_objects[i].distance * 20 * math.sin(
            math.radians(object_list.list_of_objects[i].angle)))

        new_frame['position (t)'][i, 1] = round(900 - object_list.list_of_objects[i].distance * 20 * math.cos(
            math.radians(object_list.list_of_objects[i].angle)))

        new_frame['id'][i] = object_list.list_of_objects[i].object_id
        # print(new_frame['id'][i])

        # Size - Diameter * Unknown
        new_frame['size'][i] = (((object_list.list_of_objects[i].width * 20) - 5) * 3 / 5) ** 2

        # Colour
        # objects_in_frame['color'][i] = object_colours[object_list.list_of_objects[i].object_id]

    # print(objects_in_frame)

    objects_in_frame = assign_objects(objects_in_frame, 10, new_frame, len(object_list.list_of_objects), 1 / 30)

    # objects_in_frame['color'] = object_colours[objects_in_frame['id']]

    objects_in_frame['color'] = object_colours[0]

    # end_frame = time.process_time()
    # calculate_velocity(j, objects_in_frame, objects_in_last_frame)
    # start_frame = time.process_time()

    # Update Scatter Plot Positions
    scatter_plot.set_offsets(objects_in_frame['position (t)'])
    scatter_plot_1.set_offsets(objects_in_frame['position (t-1)'])
    scatter_plot_2.set_offsets(objects_in_frame['position (t-2)'])
    scatter_plot_3.set_offsets(objects_in_frame['position (t-3)'])
    scatter_plot_4.set_offsets(objects_in_frame['position (t-4)'])
    scatter_plot_5.set_offsets(objects_in_frame['position (t-5)'])
    scatter_plot_6.set_offsets(objects_in_frame['position (t-6)'])

    # Update Scatter Plot Sizes
    scatter_plot.set_sizes(objects_in_frame['size'])

    # Update Scatter Plot Colours
    scatter_plot.set_facecolors(objects_in_frame['color'])
    scatter_plot.set_edgecolors(objects_in_frame['color'])


animation = FuncAnimation(fig, update, interval=33)
plt.show()
