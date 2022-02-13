import socket
import pickle
import math

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
object_heights = [1.72, 1.05, 1.6, 1.125, 19, 3.8, 4, 4, 2, 0.6,
                  0.8, 0.8, 1.7, 0.8, 0.2, 0.3, 0.4, 1.9, 0.8, 1.4]
object_colours = [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [1, 0, 0], [1, 0.85, 0], [1, 0, 0], [0, 1, 0], [0, 1, 0],
                  [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [1, 1, 0], [1, 0.85, 0], [1, 0.85, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]]

objects_in_frame = []

TCP_IP = '169.254.56.154'
TCP_PORT = 5005
BUFFER_SIZE = 1024


def object_distance(object_id, object_height_pixels):
    object_height_on_sensor_mm = total_sensor_height_mm * object_height_pixels / total_sensor_height_pixels
    distance_to_object = round(object_heights[object_id] * sensor_focal_length_mm / object_height_on_sensor_mm, 3)
    print(object_names[object_id], " is ", distance_to_object, "meters away")
    return distance_to_object


def object_angle(object_id, x_location):
    angle_to_object = round(
        (x_location - (total_sensor_width_pixels / 2)) * (sensor_field_of_view_degrees / total_sensor_width_pixels), 3)
    print(object_names[object_id], " is @ ", angle_to_object, "°")
    return angle_to_object


def object_width(object_id, object_height_pixels, object_width_pixels):
    object_width_m = round(object_width_pixels * object_heights[object_id] / object_height_pixels, 3)
    return object_width_m


class Object:
    def __init__(self, object_id, object_height_pixels, object_width_pixels, object_x_location):
        self.object_id = object_id
        self.distance = object_distance(object_id, object_height_pixels)
        self.angle = object_angle(object_id, object_x_location)
        self.width = object_width(object_id, object_height_pixels, object_width_pixels)


class ObjectList:
    def __init__(self, list_of_objects):
        self.list_of_objects = list_of_objects


def send_objects(object_to_send):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    print("Sending Packet ")
    s.send((pickle.dumps(object_to_send)))
    s.close()
