# RMSE (Root Mean Squared Error)
# for ``unfold`` by dandy garda

import os
import json
import collections
import math

# Save into json
def saveData(name, data):
    if not os.path.exists(os.getcwd() + '\\result-rmse'):
        os.makedirs('result-rmse')
    with open("./result-rmse/"+ str(name) +".json", 'w+') as result:
        json.dump(data, result)
        print("\nSaved in " + './result-rmse/' + str(name) + '.json', end="\n")

# Compare class/list between json
def compareList(l1, l2):
    sorted(l1)
    sorted(l2)
    if(l1 == l2):
        return True
    else:
        return False

# Find frequency from array using python collections
def frequencyValue(arr):
    convertRound = map(lambda x: round(x, 2), arr)
    elem_count = collections.Counter(convertRound)
    
    for key, value in elem_count.most_common(1):
        return key, value

# Measure RMSE
def measureRMSE(arr, actual_arr):
    rmse = 0

    for i in range(len(arr)):
        subsActForc = (float(actual_arr[i]) - float(arr[i]))
        rmse = rmse + (math.pow((subsActForc), 2))

    rmse = rmse / len(arr)

    return math.sqrt(rmse)

# Template error related from RMSE
def errorMessage(msg):
    print("\n\033[91mERRRRRR!!\033[0m")
    print("Message: " + msg)
    quit()