# 3rd Year Project - Object Detection for Autonomous Vehicles

<p align="center">
  <img src="https://user-images.githubusercontent.com/93823322/156553980-db5461c1-d0eb-4860-9eaa-010da036b35f.jpg" />
</p>

In recent years, autonomous driving and the integration of sensors into cars has been a growing trend. This project utilises computer vision looking both inward (at the driver), and outwards (at the road, pedestrians, other cars, etc.) to make driving safer. 

This project aims to do this computation on a commercial off-the-shelf system that can be embedded into a car, with potential for further expansion to cover up to the full 360° field of vision. 

<details closed>
<summary>Road Monitoring</summary>
  
## Road Monitoring

![image](https://user-images.githubusercontent.com/93823322/155022151-165847e3-7d62-44d9-99dd-51b0b367f47d.png)

YOLO Object detection works in 3 steps first dividing the image into a grid, checking if an object, or part of an object, is likely to exist in that square. If the probability is high enough, YOLO will interpret it as an object of the detected class, and then the original image/video can be annotated by drawing a box around that item and labelling it.
  
While seeing objects is all well and good, it is crucial to be able to tell where they are. Therefore, using the specifications of the Raspberry Pi’s Camera Module, the distance to each object and the angle at which they are to the camera can then be calculated. 
  
This concludes the information recorded by the Object Detection Module, and so the data can be passed on to the surround view system via ethernet. 

</details>

<details closed>
<summary>Surround View</summary>
  
## Surround View

![image](https://user-images.githubusercontent.com/93823322/155022253-d4c3cdbd-b9ab-4a21-9dc2-d0e1895de866.png)

The data obtained from the individual Raspberry Pi and Camera Module can be converted into coordinates relative to the car. These are plotted on a diagram to display the different objects in the vehicle’s current field of view. 
  
Basic object memory is implemented here, allowing for the speed of each object to calculated, giving the vehicle’s ‘brain’ even more data to work with. 
This application can, in conjunction with the data from the driver monitoring, to help warn the driver of impending collisions or dangers and could theoretically even allow for reactions to certain situations if implemented in an autonomous vehicle.  

</details>

<details closed>
<summary>Driver Monitoring</summary>
  
## Driver Monitoring
  
![image](https://user-images.githubusercontent.com/93823322/156554784-50cd817c-4f5a-48f0-99b6-99550002c273.png)

OpenCV object detection works by taking in an image that has been converted into grayscale and using a Haar-Cascade Classifier to detect if the object is in the image. This Haar Classifier is an algorithm that has been trained using 'positives' and 'negatives', where the 'positives' are images of the object one wishes to detect, and 'negatives' are other images that don't contain the object.
  
In this case two Haar Classifiers are used; one for facial detection and another for eye detection. For an eye to be detected, it must be found within the bounds of a detected face, which prevents many false positives.
  
The video stream from the camera that is facing the driver provides the images to monitor how awake they are. If the driver is noticed to be blinking more or for longer than the average person, then they will be alerted that they are not as awake as they should be.
  
The driver's face and eyes are demarcated using rectangles of different colours, which indicate where they are in the image.
  
If the object detection outside of the vehicle notices that the vehicle is getting too close to outside objects, such as people or other vehicles, the sensitivity of the driver monitoring system will be increased. This ensures the driver is alert enough to react to any threats on the road.

</details>

<details closed>
<summary>Hardware</summary>
  
## Hardware

<p>
   <img height="350" src="https://user-images.githubusercontent.com/93823322/156555082-ea35a796-018c-465a-b47c-142308561258.png"></a>
</p>
  
The Raspberry Pi 4 8GB, along with its Camera Module, was chosen as the embedded system of choice due to its affordability despite its lack of processing capabilities. 

</details>

<details closed>
<summary>Software</summary>
  
## Software

![image](https://user-images.githubusercontent.com/93823322/155022458-eec976e1-46fe-4f79-8085-ca2b3383c2ee.png)

You Only Look Once v5 (YOLOv5) is a lightweight object detection algorithm designed to be used in real time. YOLOv5 was chosen as it contains many different variants, including YOLOv5-nano, a much smaller and hence less computationally complex model of YOLO. 

YOLOv5 is also the most up to date version with an active development community.

![image](https://user-images.githubusercontent.com/93823322/155022481-fc620fb1-4396-4747-9268-9f80523607c1.png)

OpenCV or Open Source Computer Vision Library, is an extensive library mostly targeting real-time computer vision applications. With C++, Python and Java interfaces, along with support for all major operating systems, OpenCV is incredibly popular in the computer vision world. 

</details>

<details closed>
<summary>Installing YOLOv5 / YOLOv5-Lite</summary>
  
## Installing YOLOv5 / YOLOv5-Lite

`git clone https://github.com/thanley4/yolov5`
or
`git clone https://github.com/thanley4/YOLOv5-Lite`

`cd YOLOv5-Lite`

`pip install -r requirements.txt`

### Raspberry Pi 4B (ARM)

`git clone https://github.com/thanley4/PyTorch-and-Vision-for-Raspberry-Pi-4B`

`cd PyTorch-and-Vision-for-Raspberry-Pi-4B`

`pip install torch-1.8.0a0+56b43f4-cp37-cp37m-linux_armv7l.whl`

`pip install torchvision-0.9.0a0+8fb5838-cp37-cp37m-linux_armv7l.whl`

Edit requirements.txt and replace 

```
scipy>=1.4.1

torch>=1.7.0

torchvision>=0.8.1

tqdm>=4.41.0
```

with 

```
scipy>=1.4.1

torch

torchvision

tqdm>=4.41.0
```
  
</details>

<details closed>
<summary>Running YOLOv5 / YOLOv5-Lite</summary>

## Running w/ Webcam/Raspberry Pi Camera Module

`cd YOLOv5-Lite`
or
`cd yolov5`

`python3 detect.py --source 0`


## Running surround_view.py w/ Webcam/Raspberry Pi Camera Module (YOLOv5 only)

`git clone https://github.com/thanley4/3rdYearProject/`

`cd 3rdYearProject`
 
Check IP Addresses match the Local IP/Network IP in surround_view.py and detect.py

`python3 surround_view.py`

In a seperate command window/terminal

`cd YOLOv5`

`python3 detect.py --source 0`
 

</details>


## Original Repositories

YOLOv5 => https://github.com/ultralytics/yolov5

YOLOv5-Lite => https://github.com/ppogg/YOLOv5-Lite

torch 1.8.0 for Raspberry Pi 4B => https://github.com/sungjuGit/PyTorch-and-Vision-for-Raspberry-Pi-4B

torchvision 0.9.0 for Raspberry Pi 4B => https://github.com/sungjuGit/PyTorch-and-Vision-for-Raspberry-Pi-4B

