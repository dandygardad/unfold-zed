# Root Mean Squared Error (compiler)
# # for ``unfold`` by dandy garda

import os
import yaml
import pandas as pd
import time

from helper.rmse import *



print("\n== RESULT OF RMSE (Root Mean Squared Error) ==\n``unfold`` by dandy garda\n")



##### LOAD CONFIG FROM changeData #####

f = open('config.yaml')
config = yaml.safe_load(f)
f.close()

strictClass = config['rmse']['strictClass']

#### END OF LOAD CONFIG FROM changeData #####




##### LOAD FILE FROM result-rmse #####

f = os.listdir("./result-rmse")

# Make variable contain actual dist
def splitDist(n):
    return n.split('.')[0]

actual_dist = list(map(splitDist, f))

##### END OF LOAD FILE FROM result-rmse #####




##### COMPARE CLASSES START FROM FIRST JSON #####

data = dict()
path_one = os.path.join(os.getcwd(), "result-rmse", f[0])

with open(path_one) as file:
    rmse_json_one = json.load(file)

dict_rmse_json_one = list(rmse_json_one.keys())

data[actual_dist[0]] = dict()
for key in dict_rmse_json_one:
    value, _ = frequencyValue(rmse_json_one[key])
    print("Jarak yang dominan untuk " + str(key) + ' pada ' + f[0] + ' = ' + str(value))
    data[actual_dist[0]] = {**data[actual_dist[0]], key: value }

for i in range(len(f)):
    if i == 0:
        continue

    path = os.path.join(os.getcwd(), "result-rmse", f[i])
    
    with open(path) as file:
        rmse_json = json.load(file)

    dict_rmse_json = list(rmse_json.keys())

    # Check if there is same class (can changed at config.yaml)
    if strictClass:
        is_same = compareList(dict_rmse_json_one, dict_rmse_json)
        if not is_same:
            errorMessage(f[0] + " and " + f[i] + " have different classes!")
            exit()

    # Append
    data[actual_dist[i]] = {}
    for key in dict_rmse_json:
        value, _ = frequencyValue(rmse_json[key])
        print("Jarak yang dominan untuk " + str(key) + ' pada ' + f[i] + ' = ' + str(value))
        data[actual_dist[i]] = {**data[actual_dist[i]], key: value}

print()

##### END OF COMPARE CLASSES START FROM FIRST JSON #####




##### MEASURE RMSE #####

result_rmse = dict()
forc_rmse = dict()

# Fetch all class
for dist in data:
    for key in data[dist]:
        result_rmse[key] = 0
        forc_rmse[key] = list()
        
for dist in data:
    for key in data[dist]:
        forc_rmse[key].append(data[dist][key])

for arr in forc_rmse:
    rmse = measureRMSE(forc_rmse[arr], actual_dist)
    result_rmse[arr] = rmse


# Show result
print("- Hasil RMSE yang didapatkan -")
for key in result_rmse:
    print(f"{key} : {result_rmse[key]}")

# Export to csv and excel
filename = time.time()
if not os.path.exists(os.getcwd() + '\\result'):
    os.makedirs('result')

df = pd.DataFrame(result_rmse, index=[0])

df.to_csv(os.getcwd() + '/result/' + str(int(filename)) + '.csv')
print("\nSaved result: " + os.getcwd() + '/result/'+ str(int(filename)) + '.csv')

df.to_excel(os.getcwd() + '/result/' + str(int(filename)) + '.xlsx', index=False)
print("Saved result: " + os.getcwd() + '/result/'+ str(int(filename)) + '.xlsx')

##### END OF MEASURE RMSE #####