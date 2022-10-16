# Stereoscopic Measurement
# for ``unfold`` by dandy garda

import math
import cv2
import yaml
from helper.general import errorMessage



# Import config
config = yaml.safe_load(open('./config.yaml'))


# Create manual bbox label and distance
def bboxLabelDistance(dataBbox, data, frame):
    i = 0
    while i < len(data):
        label = data.iloc[i]['class']
        distance = round(data.iloc[i]['distance'], 2)

        if distance < config['distanceConfig']['min']:
            distance = 'Too close!'
        elif distance > config['distanceConfig']['max']:
            distance = 'Too far!'
        else:
            distance = str(distance)
        
        xmin = int(dataBbox.iloc[i]['xmin'])
        ymin = int(dataBbox.iloc[i]['ymin'])
        xmax = int(dataBbox.iloc[i]['xmax'])
        ymax = int(dataBbox.iloc[i]['ymax'])

        if config['cameraConfig']['resolution'] == "HD1080":
            text_size, _ = cv2.getTextSize(label + ' ' + distance, cv2.FONT_HERSHEY_SIMPLEX, 3, 4)
            text_w, text_h = text_size

            resultImg = cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            resultImg = cv2.rectangle(frame, (xmin, ymin), (xmin + text_w, ymin - text_h), (0, 0, 0), -1)
            resultImg = cv2.putText(frame, label + ': ' + distance, (xmin, ymin-5), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        elif config['cameraConfig']['resolution'] == "HD720":
            text_size, _ = cv2.getTextSize(label + ' ' + distance, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)
            text_w, text_h = text_size

            resultImg = cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            resultImg = cv2.rectangle(frame, (xmin, ymin), (xmin + text_w, ymin - text_h), (0, 0, 0), -1)
            resultImg = cv2.putText(frame, label + ': ' + distance, (xmin, ymin-5), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        elif config['cameraConfig']['resolution'] == "VGA":
            text_size, _ = cv2.getTextSize(label + ' ' + distance, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            text_w, text_h = text_size

            resultImg = cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            resultImg = cv2.rectangle(frame, (xmin, ymin), (xmin + text_w, ymin - text_h), (0, 0, 0), -1)
            resultImg = cv2.putText(frame, label + ': ' + distance, (xmin, ymin-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
        i += 1

    return resultImg

    

# Converting the results from PyTorch hub
def convertBbox(x1, y1, x2, y2):
    xc = (x1 + x2) / 2
    yc = (y1 + y2) / 2
    width = (x2 - x1)
    height = (y2 - y1)

    return xc, yc, width, height


# Stereoscopic Measurement
"""
PARAMETERS:

leftX = target coordinates in the x-axis for left camera (px)
rightX = target coordinates in the x-axis for right camera (px)
width = width taken from image dimension (px)
b = baseline (actual distance between two cameras) (m)
fov = field of view/lens view angle (two cameras must be of the same model)
"""

# kamera zed (person) - 2.0
# kamera zed (motorcycle) - 3.0
# kamera zed (car) - 1.5
def stereoscopicMeasurement(leftX, rightX, width, b, fov):
    baselineWidth = float(b) * float(width)
    disparity = round(abs(float(leftX) - float(rightX)), config['cameraConfig']['detectRound']) 
    fieldOfView = float(math.tan(math.radians(fov / 2)))
    # fieldOfView = 0.9   # HD1080
    # fieldOfView = 1.15   # HD720
    # fieldOfView = 1.25   # VGA
    # + 0.88727

    print("\nBaseline x width: " + str(baselineWidth))
    print("Disparity: " + str(disparity))
    print("Field of View: " + str(fieldOfView))
    
    try:
        distance = baselineWidth / ((2 * fieldOfView) * disparity)
    except ZeroDivisionError:
        distance = 0
        
    return distance, disparity