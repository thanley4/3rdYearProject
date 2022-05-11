import math
import random
from PIL import Image, ImageDraw
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
object_colours = ["red", "orange", "yellow"]

objects_in_frame = []


def object_distance(object_id, object_height_pixels):
    object_height_on_sensor_mm = total_sensor_height_mm * object_height_pixels / total_sensor_height_pixels
    distance_to_object = round(object_heights[object_id] * sensor_focal_length_mm / object_height_on_sensor_mm, 3)
    print(object_names[object_id], " is ", distance_to_object, "meters away")
    return distance_to_object


def object_angle(object_id, x_location):
    angle_to_object = round((x_location - (total_sensor_width_pixels / 2)) * (sensor_field_of_view_degrees / total_sensor_width_pixels), 3)
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


def drawObjects(objects, image_path, output_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    colors = ["red", "green", "blue", "yellow", "purple", "orange"]

    points = [(417, 0), (960, 900), (1503, 0)]
    draw.line(points, width=5, fill="gray", joint="curve")
    draw.arc((860, 800, 1060, 1000), start=-121.1, end=-58.9, width=1, fill="gray")
    draw.arc((760, 700, 1160, 1100), start=-121.1, end=-58.9, width=1, fill="gray")
    draw.arc((660, 600, 1260, 1200), start=-121.1, end=-58.9, width=1, fill="gray")
    draw.arc((560, 500, 1360, 1300), start=-121.1, end=-58.9, width=1, fill="gray")
    draw.arc((460, 400, 1460, 1400), start=-121.1, end=-58.9, width=1, fill="gray")
    draw.arc((360, 300, 1560, 1500), start=-121.1, end=-58.9, width=1, fill="gray")
    draw.arc((260, 200, 1660, 1600), start=-121.1, end=-58.9, width=1, fill="gray")
    draw.arc((160, 100, 1760, 1700), start=-121.1, end=-58.9, width=1, fill="gray")
    draw.arc(( 60, 000, 1860, 1800), start=-121.1, end=-58.9, width=1, fill="gray")
    draw.arc((-40, -100, 1960, 1900), start=-121.1, end=-58.9, width=1, fill="gray")

    '''
    for i in objects:
        x = 960 + i.distance * 10 * math.sin(math.radians(i.angle))
        y = 900 - i.distance * 10 * math.cos(math.radians(i.angle))
        draw.ellipse((x - (10 * i.width / 2), y - (10 * i.width / 2), x + (10 * i.width / 2), y + (10 * i.width / 2)), fill=object_colours[i.object_id])
    '''

    image.save(output_path)
    image.show(image)



if __name__ == "__main__":
    i = 0
    while i < 10:
        objects_in_frame.clear()
        objects_in_frame.append(Object(0, random.randint(10, 100), random.randint(100, 200), random.randint(0, 3280)))
        objects_in_frame.append(Object(1, random.randint(10, 100), random.randint(100, 200), random.randint(0, 3280)))
        objects_in_frame.append(Object(2, random.randint(10, 100), random.randint(100, 200), random.randint(0, 3280)))
        drawObjects(objects_in_frame, "Field_of_View.jpg", "Field_of_View_Output.jpg")
        i = i + 1