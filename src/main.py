from fileinput import filename
import sys
from functions import filterData, computeTherapySimilarity, computeConditionsSimilarity, produceOutput
from functions import combineSimilarities, predictRatings, fiveMostEfficient
from classes import Condition, Therapy, Patient
import numpy as np
import warnings
import time

#ignore the warning of division by zero in cosine similarity (if divided by zero the similarity is 0 so we do not care)
warnings.filterwarnings('ignore')

#read information from prompt dataset from prompt
# filename = sys.argv[1]
# patientID = sys.argv[2]
# conditionID = sys.argv[3]

filename = input("Insert data/datasetA.json or data/datasetB.json")
patientID = input("Insert the ID of the patient ")
conditionID = input("Insert the id of the condition ")

#@patients --> list of patients instances
#@trials --> list of trials
#@conditions --> list of conditions
#@target --> Patient instance of the target patient
patients, trials, conditions, target = filterData(filename, patientID, conditionID)

#@T_matrix --> matrix for therapy based similarity
T_matrix = np.zeros((len(patients), len(trials)+1))
#@C_matrix --> matrix for conditions based similarity
C_matrix = np.zeros((len(patients), len(conditions)+1))

#@T_similarities --> vector of similarities therapy-based approach
#@target_vector --> vector of therapies of the target patient
T_similarities, target_vector = computeTherapySimilarity(patients, target, T_matrix)

#@C_similarities --> vector of similarities condition-based approach
C_similarities = computeConditionsSimilarity(patients, target, C_matrix)

#@similarities --> vector of combined similarities
similarities = combineSimilarities(T_similarities, C_similarities)

#@ratings --> vector of predicted ratings
ratings = predictRatings(similarities, T_matrix, target_vector)

#@five_therapies --> vector of ids of the best five therapies
five_therapies = fiveMostEfficient(ratings)

#produce the output of the algorithm
produceOutput(five_therapies, trials)

time.sleep(5)






