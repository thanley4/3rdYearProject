# 3rd Year Project - Object Detection for Autonomous Vehicles

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

## Running w/ Webcam/Raspberry Pi Camera Module

`cd YOLOv5-Lite`
or
`cd yolov5`

`python3 detect.py --source 0`


## Running surround_view.py w/ Webcam/Raspberry Pi Camera Module (YOLOv5 only)

`git clone https://github.com/thanley4/3rdYearProject/`

`cd 3rdYearProject`

`python3 surround_view.py`

In a seperate command window/terminal

`cd YOLOv5`

`python3 detect.py --source 0`


## Original Repositories

YOLOv5 => https://github.com/ultralytics/yolov5

YOLOv5-Lite => https://github.com/ppogg/YOLOv5-Lite

torch 1.8.0 for Raspberry Pi 4B => https://github.com/sungjuGit/PyTorch-and-Vision-for-Raspberry-Pi-4B

torchvision 0.9.0 for Raspberry Pi 4B => https://github.com/sungjuGit/PyTorch-and-Vision-for-Raspberry-Pi-4B

