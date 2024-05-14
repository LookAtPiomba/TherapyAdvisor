To execute the algorithm:
1) Download the folder and in case unzip it.
2) open a shell and go inside the folder you downloaded.
3) execute the following command: python 'src/main.py' 'data/{datasetname}.json' '{patientID}' '{conditionID}'
	-{datasetname} has to be either "datasetA" or "datasetB";
	-{patientID} is the ID of the target patient in the dataset;
	-{conditionID} could be both the condition id in the patients lists("pc...") or the id of 
		the condition in the list of conditions ("Cond...").

To run the test, just simply replace test.py instead of main.py
