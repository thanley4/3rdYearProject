import numpy as np
from matplotlib.animation import FuncAnimation
import math
import random
import matplotlib.pyplot as plt

total_sensor_height_mm = 2.76  # mm
total_sensor_width_mm = 3.68  # mm
total_sensor_height_pixels = 2464  # pixels
total_sensor_width_pixels = 3280  # pixels
sensor_focal_length_mm = 3.04  # mm
sensor_field_of_view_degrees = 62.2  # degrees

object_names = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light",
                "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
                "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
                "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
                "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
                "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
                "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard",
                "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
                "scissors", "teddy bear", "hair drier", "toothbrush"]
object_heights = [1.72, 1.05, 1.6]
object_colours = ['r', 'b', 'y']

objects_in_frame = []
plotting_data_x = []
plotting_data_y = []
plotting_data_size = []
plotting_data_colour = []


def object_distance(object_id, object_height_pixels):
    object_height_on_sensor_mm = total_sensor_height_mm * object_height_pixels / total_sensor_height_pixels
    distance_to_object = round(object_heights[object_id] * sensor_focal_length_mm / object_height_on_sensor_mm, 3)
    # print(object_names[object_id], " is ", distance_to_object, "meters away")
    return distance_to_object


def object_angle(object_id, x_location):
    angle_to_object = round(
        (x_location - (total_sensor_width_pixels / 2)) * (sensor_field_of_view_degrees / total_sensor_width_pixels), 3)
    # print(object_names[object_id], " is @ ", angle_to_object, "°")
    return angle_to_object


def object_width(object_id, object_height_pixels, object_width_pixels):
    object_width_m = round(object_width_pixels * object_heights[object_id] / object_height_pixels, 3)
    # print(object_names[object_id], " is ", object_width_m, "meters wide")
    return object_width_m


class Object:
    def __init__(self, object_id, object_height_pixels, object_width_pixels, object_x_location):
        self.object_id = object_id
        self.distance = object_distance(object_id, object_height_pixels)
        self.angle = object_angle(object_id, object_x_location)
        self.width = object_width(object_id, object_height_pixels, object_width_pixels)


def create_objects():
    objects_in_frame.clear()
    for j in range(0, random.randint(10, 10)):
        objects_in_frame.append(
            Object(random.randint(0, 2), random.randint(10, 100), random.randint(100, 200), random.randint(0, 3280)))
        plt.pause(0.1)
    return objects_in_frame


# def plot_objects():

img = plt.imread("Background.jpg")

# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(16, 9), dpi=120)

ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0.0, 1920), ax.set_xticks([])
ax.set_ylim(1080, 0.0), ax.set_yticks([])
#ax.imshow(img)

# Create rain data
constant = 100

plot = np.zeros(constant, dtype=[('position', float, (2,)),
                                 ('y', int),
                                 ('size', int),
                                 ('colour', int, (3,))])

# Initialize the raindrops in random positions and with
# random growth rates.
plot['position'][:, 0] = -1000
plot['position'][:, 1] = -1000
plot['size'] = 10

# Construct the scatter which we will update during animation
# as the raindrops develop.
scatter_plot = ax.scatter(plot['position'][:, 0], plot['position'][:, 1], plot['size'])


def update(me):
    print("update")
    create_objects()

    plot['position'][:, 0] = -1000
    plot['position'][:, 1] = -1000
    plot['size'] = 10

    for i in range(0, 10):
        print(objects_in_frame)
        plot['position'][:, 0][i] = int(960 + i.distance * 10 * math.sin(math.radians(i.angle)), 0)
        plot['position'][:, 1][i] = int(900 - i.distance * 10 * math.cos(math.radians(i.angle)), 0)
        plot['size'][i] = np.random.uniform(0, 25, i.width)
        print("objects")

    scatter_plot.set_offsets(plot['position'])
    scatter_plot.set_sizes(plot['size'])


animation = FuncAnimation(fig, update, interval=100)
plt.show()
