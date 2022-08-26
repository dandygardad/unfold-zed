# General functions
# for ``unfold`` by dandy garda

import cv2
import os

# Header template
def unfoldHeader(cls):
    if cls:
        os.system('cls')
    else:
        print('\n')
    print('\033[92m``unfold with zed stereo``\033[0m v.1.1.0')
    print('\033[1mA Python project for measuring distance between two ships with ZED Stereo Camera.\033[0m')
    print('\n\033[1mmade by Dandy Garda\033[0m')
    print('\033[1mgowa, 2022\033[0m')
    print('\n-----------------------------------------------------------------------------\n')


# Template for error message
def errorMessage(msg):
    print("\n\033[91mERRRRRR!!\033[0m")
    print("Message: " + msg)
    quit()

# Check original dimension
def originalDimCheck(cam):
    return round(cam.get_camera_information().camera_resolution.width, 2), round(cam.get_camera_information().camera_resolution.height, 2), round(cam.get_camera_information().camera_resolution.width, 2), round(cam.get_camera_information().camera_resolution.height, 2)

# Template error related from detection
def errorDetection(msg, frameL, frameR):
    print("\nERRRR: " + msg)
    return frameL, frameR