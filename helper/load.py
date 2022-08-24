# Functions to help stereo camera running and calibrated
# for ``unfold`` by dandy garda

import cv2
import os
import yaml
import pyzed.sl as sl
from helper.general import originalDimCheck, errorMessage

config = yaml.safe_load(open('./config.yaml'))

def zedStereo():
    init = sl.InitParameters()



    # Change resolution & FPS (https://www.stereolabs.com/docs/video/camera-controls/#using-the-api)

    if(config['cameraConfig']['resolution'] == "VGA"):
        init.camera_resolution = sl.RESOLUTION.VGA
    elif(config['cameraConfig']['resolution'] == "HD720"):
        init.camera_resolution = sl.RESOLUTION.HD720
    elif(config['cameraConfig']['resolution'] == "HD1080"):
        init.camera_resolution = sl.RESOLUTION.HD1080
    else:
        errorMessage("Cannot open webcam!")

    init.camera_fps = 30

    # End of change resolution & FPS



    runtime = sl.RuntimeParameters()

    cam = sl.Camera()
    
    if not cam.is_opened:
        errorMessage("Cannot open webcam!")

    status = cam.open(init)

    if status != sl.ERROR_CODE.SUCCESS:
        errorMessage("Cannot open webcam!")
        
    # Show original dimension
    widthL, heightL, widthR, heightR = originalDimCheck(cam)

    print("\nVideo 1 original dimension: " + str(widthL) + ' ' + str(heightL))
    print("Video 2 original dimension: " + str(widthR) + ' ' + str(heightR))

    print("\nSuccess: Stereo Camera successfully loaded!")

    return cam, runtime, widthL, heightL, widthR, heightR