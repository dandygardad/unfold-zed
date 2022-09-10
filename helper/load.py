# Functions to help stereo camera running and calibrated
# for ``unfold`` by dandy garda

import cv2
import os
import yaml
import pyzed.sl as sl
from helper.general import originalDimCheck, errorMessage

f = open('./config.yaml')
config = yaml.safe_load(f)
f.close()

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

def stereoCamera(L, R, dshow):
    if dshow:
        camL = cv2.VideoCapture(L, cv2.CAP_DSHOW)
        camR = cv2.VideoCapture(R, cv2.CAP_DSHOW)
    else:
        camL = cv2.VideoCapture(L)
        camR = cv2.VideoCapture(R)

    if not camL.isOpened() & camR.isOpened():
        errorMessage("Cannot open webcam!")

    # Show original dimension
    widthL, heightL, widthR, heightR = originalDimCheck(camL)

    print("\nVideo 1 original dimension: " + str(widthL) + ' ' + str(heightL))
    print("Video 2 original dimension: " + str(widthR) + ' ' + str(heightR))

    print("\nSuccess: Stereo Camera successfully loaded!")

    return camL, camR, widthL, heightL, widthR, heightR