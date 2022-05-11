import math
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation


f = plt.figure(figsize=(16, 9), dpi=120)

plt.xlim([0, 1920])
plt.ylim([0, 1080])
plt.box(False)
plt.axis(False)
img = plt.imread("Background.jpg")


ax = f.add_axes([0, 0, 1, 1])
ax = plt.gca()
ax.set_xlim(0.0, 1920)
ax.set_ylim(1080, 0.0)
ax.imshow(img)

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
    #print(object_names[object_id], " is ", distance_to_object, "meters away")
    return distance_to_object


def object_angle(object_id, x_location):
    angle_to_object = round((x_location - (total_sensor_width_pixels / 2)) * (sensor_field_of_view_degrees / total_sensor_width_pixels), 3)
    #print(object_names[object_id], " is @ ", angle_to_object, "°")
    return angle_to_object


def object_width(object_id, object_height_pixels, object_width_pixels):
    object_width_m = round(object_width_pixels * object_heights[object_id] / object_height_pixels, 3)
    #print(object_names[object_id], " is ", object_width_m, "meters wide")
    return object_width_m


class Object:
    def __init__(self, object_id, object_height_pixels, object_width_pixels, object_x_location):
        self.object_id = object_id
        self.distance = object_distance(object_id, object_height_pixels)
        self.angle = object_angle(object_id, object_x_location)
        self.width = object_width(object_id, object_height_pixels, object_width_pixels)


def animate(i):
    if i < 10:
        create_objects()
        draw_objects(objects_in_frame)


def create_objects():
    objects_in_frame.clear()
    for j in range(0, random.randint(3, 10)):
        objects_in_frame.append(Object(random.randint(0, 2), random.randint(10, 100), random.randint(100, 200), random.randint(0, 3280)))
        plt.pause(0.1)
    return objects_in_frame


def draw_objects(objects):
    colors = ["r", "g", "b", "y", "p", "o"]
    plotting_data_x.clear()
    plotting_data_y.clear()
    plotting_data_size.clear()
    plotting_data_colour.clear()

    for i in objects:
        x = round(960 + i.distance * 10 * math.sin(math.radians(i.angle)))
        y = round(900 - i.distance * 10 * math.cos(math.radians(i.angle)))
        plotting_data_x.append(x)
        plotting_data_y.append(y)
        plotting_data_size.append(int(i.width * 5))
        plotting_data_colour.append(colors[i.object_id])
        #circle = plt.Circle((x, y), radius=(i.width * 5), fc=colors[i.object_id])
        #plt.gca().add_patch(circle)

    plt.scatter(plotting_data_x, plotting_data_y, plotting_data_size, plotting_data_colour)


animation = animation.FuncAnimation(f, animate, blit=True)
plt.show()
print("end")
