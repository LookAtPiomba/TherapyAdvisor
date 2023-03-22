import sys
import json
from functions import produceOutput
from classes import Condition, Therapy, Patient
import numpy as np

#handles different input of conditionID
def adjustConditionID(pcID, patientID, db):
    for x in db['Patients']:
        if str(x['id']) == patientID:
            for y in x['conditions']:
                if y['id'] == pcID:
                    return y['kind']  

#read information from prompt dataset from prompt
filename = sys.argv[1]
patientID = sys.argv[2]
conditionID = sys.argv[3]

stream = open(filename)
db = json.load(stream)
stream.close()

if "pc" in conditionID:
        conditionID = adjustConditionID(conditionID, patientID, db)

trials = [x for x in db["Therapies"]]
v = np.zeros(len(trials)+1)
h = 0
for p in db["Patients"]:
    for c in p["conditions"]:
        if c['kind'] == conditionID and (c['cured'] != None and c['cured'] != "Null"):
            for t in p["trials"]:
                if t["condition"] == c["id"]:
                    if int(t['successful']) >= 75:
                        i = t["therapy"].replace("Th","")
                        v[int(i)]+=1

print(v)
v = v.tolist()

#save the indexes of the best five therapies
five_therapies = np.zeros(5)
for i in range(5):
    max_i = v.index(max(v))
    v[max_i] = 0
    five_therapies[i] = max_i

#produces the output
produceOutput(five_therapies, trials)

