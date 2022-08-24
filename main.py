# Main application
# for ``unfold`` by dandy garda

# Import libraries and functions
import pandas as pd
import cv2
import torch
import yaml
import os
import pyzed.sl as sl

from helper.general import unfoldHeader, errorMessage, errorDetection
from helper.load import zedStereo
from helper.distance import convertBbox, stereoscopicMeasurement, bboxLabelDistance
from helper.rmse import saveData







###### LOAD YAML ######

f = open('config.yaml')
dataConfig = yaml.safe_load(f)
f.close()

# ``unfold`` Header
unfoldHeader(dataConfig['header']['cls'])

# Load data from yaml
if dataConfig['cameraConfig']['model']:
    # Custom model
    model_custom = './models/' + dataConfig['cameraConfig']['model']
else:
    # Default model by YOLOv5 (Coco128)
    model_custom = './models/' + 'yolov5s.pt'

if dataConfig['cameraConfig']['conf']:
    conf_custom = dataConfig['cameraConfig']['conf']
else:
    conf_custom = 0

if dataConfig['rmse']['mode']:
    mode_rmse = dataConfig['rmse']['mode']
    dist_rmse = dataConfig['rmse']['setDistance']
    frame_rmse = dataConfig['rmse']['maxFramesPerDist']
    result_rmse = {}
    distances_rmse = list()

    print("INGFO: Mode RMSE ON!\n")
else:
    mode_rmse = False

###### END OF LOAD YAML ######




###### LOAD STEREO CAMERA ######

print("=== LOAD STEREO CAMERA ===")
cam, runtime, widthL, heightL, widthR, heightR = zedStereo()
    
# Assume two cameras are same model
dim = (widthL, heightL)

###### END OF LOAD STEREO CAMERA ######




###### LOAD YOLOv5 ######

print("\n\n=== RUNNING YOLOv5 ===")
try:
    model = torch.hub.load('yolov5-detect', 'custom', path=model_custom, source='local')
except Exception as e:
    print(e)
    errorMessage("Cannot load model, please check 'torch.hub.load' function!")

###### END OF LOAD YOLOv5 ######




###### RUN YOLOv5 TO OpenCV ######

print("\n\n=== PUT YOLOv5 INTO STEREO CAMERA ===")
print("=== APPLY DISTANCE MEASUREMENT ===")
initial_frame = 0

while True:
    if mode_rmse:
        print("\nFrame: " + str(initial_frame))
        if initial_frame == frame_rmse:
            saveData(dist_rmse, result_rmse)
            break

    classes = list()
    distances = list()
    try:
        ###### STEREO CAMERA & SETTINGS ######

        # Load stereo camera
        # retL, retR, resized1, resized2, resizedGrayL, resizedGrayR, key = resizedStereoCamera(camL, camR, stereoMapL_x, stereoMapL_y, stereoMapR_x, stereoMapR_y, dim)
        
        left_image = sl.Mat()
        right_image = sl.Mat()

        # Inference Settings
        model.conf = conf_custom

        if dataConfig['cameraConfig']['customModel'] != False:
            model.classes = dataConfig['cameraConfig']['customModel']
            

        # Load frame to model
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS :
            cam.retrieve_image(left_image, sl.VIEW.LEFT)
            result_left = left_image.get_data()
            
            cam.retrieve_image(right_image, sl.VIEW.RIGHT)
            result_right = right_image.get_data()

            # Load frame to model
            resultLR = model([result_left], augment=True)
            key = cv2.waitKey(10)


            ###### MATCH TEMPLATE ######

            labelL = resultLR.pandas().xyxy[0] # (Left Camera)
            labelR = pd.DataFrame({})

            for i in range(len(labelL)):
                image = result_left[int(labelL.iloc[i]['ymin']):int(labelL.iloc[i]['ymax']), int(labelL.iloc[i]['xmin']):int(labelL.iloc[i]['xmax'])]
                height, width, _ = image.shape[::]
                match = cv2.matchTemplate(result_right, image, cv2.TM_SQDIFF)
                _, _, minloc, maxloc = cv2.minMaxLoc(match)
                data = {
                    "xmin": float(minloc[0]),
                    "ymin": float(minloc[1]),
                    "xmax": float(minloc[0] + width),
                    "ymax": float(minloc[1] + height),
                    "confidence": labelL.iloc[i]['confidence'],
                    "class": labelL.iloc[i]['class'],
                    "name": labelL.iloc[i]['name']
                }
                labelR = pd.concat([labelR, pd.DataFrame(data, index=[i])]) 
            
            ###### END OF MATCH TEMPLATE ######

        ###### END OF STEREO CAMERA & SETTINGS ######




        ###### PRINT INTO COMMAND PROMPT ######

        print("\n--------------------------------------------")

        if len(labelL) and len(labelR):
            labelR = labelR.sort_values(by=['confidence'], ascending=False)  
            if len(labelL) == len(labelR):

                for i in range(len(labelL)):
                    labelL.at[i, 'name'] = labelL.iloc[i]['name'] + str(i)
                    labelR.at[i, 'name'] = labelR.iloc[i]['name'] + str(i)
                
                print("\nDetection on Left Camera: ")
                print(labelL)
                print("\nDetection on Right Camera (from template matching): ")
                print(labelR)

                id = 0
                while id < len(labelL):
                    # Converting float into int for stability value
                    xl, yl, wl, hl = convertBbox(round(labelL.iloc[id]['xmin'], dataConfig['cameraConfig']['detectRound']), round(labelL.iloc[id]['ymin'], dataConfig['cameraConfig']['detectRound']), round(labelL.iloc[id]['xmax'], dataConfig['cameraConfig']['detectRound']), round(labelL.iloc[id]['ymax'], dataConfig['cameraConfig']['detectRound']))
                    xr, yr, wr, hr = convertBbox(labelR.iloc[id]['xmin'], labelR.iloc[id]['ymin'], labelR.iloc[id]['xmax'], labelR.iloc[id]['ymax'])

                    if dataConfig['cameraConfig']['blockDiffClass']:
                        # If two class from cameras are not same then break
                        if labelL.iloc[id]['name'] == labelR.iloc[id]['name']:
                            print("\n\nx1 for left camera = " + str(xl))
                            print("x2 for right camera = " + str(xr))

                            # Result from Distance Measurement
                            distance = stereoscopicMeasurement(xl, xr, dim[0], dataConfig['cameraConfig']['baseline'], dataConfig['cameraConfig']['fieldOfView'])
                            
                            classes.append(labelL.iloc[id]['name'])
                            distances.append(distance)

                            # Append distance into RMSE
                            if mode_rmse:
                                if not labelL.iloc[id]['name'] in result_rmse:
                                    result_rmse[labelL.iloc[id]['name']] = list()
                                result_rmse[labelL.iloc[id]['name']].append(round(distance, dataConfig['rmse']['distRound']))
                        else:
                            resultImgL, resultImgR = errorDetection("Class Left & Right is not same!", result_left, result_right)
                            break
                    else:
                        print("\n\nx1 for left camera = " + str(xl))
                        print("x2 for right camera = " + str(xr))

                        # Result from Distance Measurement
                        distance = stereoscopicMeasurement(xl, xr, dim[0], dataConfig['cameraConfig']['baseline'], dataConfig['cameraConfig']['fieldOfView'])

                        classes.append(labelL.iloc[id]['name'])
                        distances.append(distance)

                        # Append distance into RMSE
                        if mode_rmse:
                            if not labelL.iloc[id]['name'] in result_rmse:
                                result_rmse[labelL.iloc[id]['name']] = list()
                            result_rmse[labelL.iloc[id]['name']].append(distance)

                    id += 1
                initial_frame += 1

                if len(classes):
                    data = {
                        'class': classes,
                        'distance': distances
                    }

                    data = pd.DataFrame(data)
                    
                    print("\nDistance Measurement:")
                    print(data)

                    # Put manual bbox and distance in frame
                    resultImgL = bboxLabelDistance(labelL, data, result_left)
                    resultImgR = bboxLabelDistance(labelR, data, result_right)
            else:
                resultImgL, resultImgR = errorDetection("Total label in L doesn't same as total label in R", result_left, result_right)
        else:
            resultImgL, resultImgR = errorDetection("No detection on left/right camera!", result_left, result_right)

        ###### END OF PRINT TO COMMAND ######




        ###### SHOW CAMERAS IN REALTIME ######

        if dataConfig['cameraConfig']['combinedCamera']:
            # Combine two frame into one
            alpha = 0.5
            beta = (1.0 - alpha)
            combineImg = cv2.addWeighted(resultImgR, alpha, resultImgL, beta, 0.0)
            cv2.imshow("Combined Cameras", combineImg)
        else:
            if dataConfig['cameraConfig']['resolution'] == 'HD720' or dataConfig['cameraConfig']['resolution'] == 'HD1080':
                resultImgL = cv2.resize(resultImgL, (672, 376))
                resultImgR = cv2.resize(resultImgR, (672, 376))
            cv2.imshow("Left Camera", resultImgL)
            cv2.imshow("Right Camera", resultImgR)

        ###### END OF SHOW CAMERAS IN REALTIME ######

        

        # Key to exit
        if key == ord('q') or key == ord('Q'):
            if mode_rmse:
                saveData(dist_rmse, result_rmse)
            print("\n\nExited!")
            break

    except KeyboardInterrupt:
        if mode_rmse:
            saveData(dist_rmse, result_rmse)
        print("\n\nExited!")
        break

###### END OF RUN YOLOv5 TO OpenCV ######



print("\nThank you!\n:)")