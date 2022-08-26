# Root Mean Squared Error (compiler) one by one JSON
# # for ``unfold`` by dandy garda

import os
import yaml
import pandas as pd
import time

from helper.rmse import *



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
    return int(n.split('.')[0])

actual_dist = sorted(list(map(splitDist, f)))

##### END OF LOAD FILE FROM result-rmse #####




print("\n== EXTRACT JSON ==\n``unfold`` by dandy garda")

for dist in range(len(actual_dist)):
    data = dict()
    path = os.path.join(os.getcwd(), "result-rmse", str(actual_dist[dist]) + '.json')

    with open(path) as file:
        rmse_json = json.load(file)

    dict_rmse = list(rmse_json.keys())

    # Export to csv and excel
    filename = time.time()
    if not os.path.exists(os.getcwd() + '\\result'):
        os.makedirs('result')

    if not os.path.exists(os.getcwd() + '\\result\\extracted'):
        os.makedirs('result\\extracted')
    
    for key in range(len(dict_rmse)):
        individualData = {dict_rmse[key]: rmse_json[dict_rmse[key]]}
        df = pd.DataFrame(individualData, index=list(range(len(rmse_json[dict_rmse[key]]))))

        df.to_csv(os.getcwd() + '/result/extracted/' + str(int(filename)) + '_' + str(actual_dist[dist]) + "_" + dict_rmse[key] + '.csv')
        print("\nSaved result: " + os.getcwd() + '/result/'+ str(int(filename)) + '_' + str(actual_dist[dist]) + "_" + dict_rmse[key] + '.csv')

        df.to_excel(os.getcwd() + '/result/extracted/' + str(int(filename)) + '_' + str(actual_dist[dist]) + "_" + dict_rmse[key] + '.xlsx', index=False)
        print("Saved result: " + os.getcwd() + '/result/'+ str(int(filename)) + '_' + str(actual_dist[dist]) + "_" + dict_rmse[key] +  '.xlsx')



##### END OF MEASURE RMSE #####