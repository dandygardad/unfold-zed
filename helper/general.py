# General functions
# for ``unfold`` by dandy garda

import cv2
import os
import yaml

f = open('./config.yaml')
config = yaml.safe_load(f)
f.close()

# Header template
def unfoldHeader(cls):
    if cls:
        os.system('cls')
    else:
        print('\n')
    print('\033[92m``unfold with zed stereo``\033[0m v.1.3.0')
    print('\033[1mA Python project for measuring distance between two ships with ZED Stereo Camera.\033[0m')
    print('\n\033[1mmade by Dandy Garda\033[0m')
    print('\033[1mgowa, 2022\033[0m')
    print('\n-----------------------------------------------------------------------------\n')

    # Instruction for brightness & contrast
    print('=== CAMERA CONTROLS FOR BRIGHTNESS & CONTRAST ===')
    print('\nPress "]" to turn up the brightness.')
    print('Press "[" to turn down the brightness.\n')
    print('Press "." to turn up the contrast.')
    print('Press "," to turn down the contrast.\n')
    print('Press', "\"'\"", "to turn up the exposure.")
    print('Press ";" to turn down the exposure.\n')

    input('Press "ENTER" key to continue!\n\n')


# Template for error message
def errorMessage(msg):
    print("\n\033[91mERRRRRR!!\033[0m")
    print("Message: " + msg)
    quit()

# Check original dimension
def originalDimCheck(cam):
    if config['capture']['mode'] == 'video':
        return cam.get(cv2.CAP_PROP_FRAME_WIDTH), cam.get(cv2.CAP_PROP_FRAME_HEIGHT), cam.get(cv2.CAP_PROP_FRAME_WIDTH), cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    return round(cam.get_camera_information().camera_resolution.width, 2), round(cam.get_camera_information().camera_resolution.height, 2), round(cam.get_camera_information().camera_resolution.width, 2), round(cam.get_camera_information().camera_resolution.height, 2)

# Template error related from detection
def errorDetection(msg, frameL, frameR):
    print("\nERRRR: " + msg)
    return frameL, frameR