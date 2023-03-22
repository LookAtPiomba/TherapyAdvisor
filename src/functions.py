import json
import numpy as np
from classes import Patient, Therapy, Condition
from scipy.spatial import distance
import math
from sklearn.metrics import jaccard_score
import pickle

#handles different input of conditionID
def adjustConditionID(pcID, patientID, db):
    for x in db['Patients']:
        if str(x['id']) == patientID:
            for y in x['conditions']:
                if y['id'] == pcID:
                    return y['kind']  

#compare dates and return true if end1 is before start2
def isBefore(end1, start2):
    if start2 < end1:
        return True
    else:
        return False

#read the json file and return the lists of patients, conditions, trials and the istance of the target patient
def filterData(filename, patientID, conditionID):
    stream = open(filename)
    db = json.load(stream)
    stream.close()
    if "pc" in conditionID:
        conditionID = adjustConditionID(conditionID, patientID, db)
    #find patients with the target condition
    patients = []
    trials = [x for x in db["Therapies"]]
    conditions = [x["id"] for x in db["Conditions"]]
    for p in db['Patients']:
        if str(p["id"]) == patientID:
            target = Patient(p['id'], p['name'])
            for c in p['conditions']:
                cond = Condition(c['id'], c['diagnosed'], c['cured'], c['kind'])
                target.addCondition(cond)
    
                for t in p['trials']:
                    if t["condition"] == c["id"] and c["kind"] == conditionID:
                        th = Therapy(t['id'], t['start'], t['end'], t['condition'], t['therapy'], t['successful'])
                        target.addTherapy(th)

        for y in p['conditions']:
            #we consider only patients that has cured their condition
            if y['kind']==conditionID and (y['cured'] != None and y['cured'] != "Null"):
                patient = (Patient(p['id'], p['name']))
                for z in p["conditions"]:
                    if isBefore(y['cured'], z['diagnosed']):
                        patient.addCondition(Condition(z['id'], z['diagnosed'], z['cured'], z['kind']))                    
                for t in p["trials"]:
                    if t["condition"] == y["id"]:
                        th = Therapy(t['id'], t['start'], t['end'], t['condition'], t['therapy'], t['successful'])
                        patient.addTherapy(th)
                
                patients.append(patient)

    return patients, trials, conditions, target

#Manipulate strings to extract the numerical substring
def extract_number(id, to_delete):
    return id.replace(to_delete, "")

#normalize the input vector by subtracting the mean on each component
def normalize(v):
    sum_V = 0
    n = 0
    for i in range(len(v)):
        if v[i] != 0:
            sum_V += v[i]
            n = n+1

    for i in range(len(v)):
        if v[i] != 0:
            v[i] = v[i] - sum_V/n
            if v[i] == 0.0:
                v[i] = 0.00000001

    return v

#computes therapy-based similarities and return them in a vector
def computeTherapySimilarity(data, target, M):
    M_normalized = M.copy()
    target_vector = np.zeros(np.shape(M)[1])
    target_vector_normalized = np.zeros(np.shape(M)[1])
    for t in target.list_of_therapies:
        j = extract_number(t.therapy, "Th")
        target_vector[int(j)] = int(t.successful)
        target_vector_normalized[int(j)] = int(t.successful)
    
    target_vector_normalized = normalize(target_vector_normalized)

    similarities = []
    i=0
    for d in data:
        for t in d.list_of_therapies:
            j = extract_number(t.therapy, "Th")
            M[i][int(j)] = int(t.successful)
        M_normalized[i] = M[i].copy()
        M_normalized[i] = normalize(M_normalized[i]) 

        s = 1 - distance.cosine(target_vector_normalized, M_normalized[i])
        similarities.append(s)        
        i = i+1

    return similarities, target_vector

#computes conditions-based similarities and return them in a vector
def computeConditionsSimilarity(data, target, M):
    target_vector = np.zeros(np.shape(M)[1])
    for c in target.list_of_conditions:
        j = extract_number(c.kind, "Cond")
        target_vector[int(j)] = 1

    similarities = []
    i=0
    for d in data:
        for c in d.list_of_conditions:
            j = extract_number(c.kind, "Cond")
            M[i][int(j)] = 1 

        s = jaccard_score(target_vector, M[i])
        similarities.append(s)
        i = i+1

    return similarities

#perform a linear combination of similarities and return it in a vector
def combineSimilarities(sim1, sim2):
    s = np.zeros(len(sim1))
    for i in range(len(sim1)):
        s[i] = sim1[i] + 2*sim2[i]
    
    return s

#predict ratings and return the target vector filled with predictions
def predictRatings(sim, M, v):

    for i in range(np.shape(M)[1]):
        numerator = 0
        denumerator = 0
        for j in range(np.shape(M)[0]):
            if(M[j][i]) >= 1:
                numerator = numerator + sim[j]*M[j][i]
                denumerator = denumerator + sim[j]
        
        if v[i] == 0:
            if denumerator != 0:
                v[i] = numerator/denumerator
        else:
            v[i] = 0

    return v      

#return the indexes of the best 5 therapies
def fiveMostEfficient(r):   
    r = r.tolist()
    s = r.copy()
    r.sort(reverse=True)
    g = np.zeros(5)
    for i in range(len(g)):
        g[i] = s.index(r[i])

    return g

#print the output in the console
def produceOutput(th_id, therapies):
    th_id = th_id.tolist()
    th = []
    for i in range(len(th_id)):
        for t in therapies:
            id = extract_number(t["id"], "Th")
            if str(t["id"]) == "Th"+str(int(th_id[i])):
                th.append(t["name"])
    
    print("Top 5 advised therapies (descending order): ")
    c = 1
    for x in th:
        print(str(c) + ") " + str(x))
        c+=1

    # with open('bin/testcase10_datasetB.bin', 'wb') as f:
    #     pickle.dump(th, f)

