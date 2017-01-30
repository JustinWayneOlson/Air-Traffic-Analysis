'''
In each row, here is the key for indexes:
[1] Quarter
[2] Month
[3] Day
[4] Day of Week (1=Monday)
[6] Carrier
[7] Airline ID
[9] Tail Number
[10] Flight Number
[11] Origin Airport ID
[14] Origin Airport Code (3 letter)
[21] Destination Airport ID
[24] Destination Airport Code (3 letter)
[31] CRS Listed departure time, in local time
[32] Actual Departure time, in local time
[33] Departure delay. Early departures are negative numbers
[34] Departure Delay, in minutes. Is 0 if departed early
[38] Taxi time, in minutes
[39] Wheels off the ground, in local time
[40] Wheels on the ground, in local time
[41] Taxi in time, in minutes
[42] CRS Listed arrival time, in local time
[43] Actual Arrival time, in local time
[44] Arrival delay. Early arrivals are negative numbers
[45] Arrival delay, in minutes. Is 0 if arrived early
[52] CRS listed time of flight, in minutes
[53] Actual flight time, in minutes
[54] Actual time in the air, in minutes
[55] Number of flights
[56] Distance between airports, in miles
[58] Carrier delay
[59] Weather delay
[60] National air system delay
[61] Security delay
[62] Late aircraft delay
'''
import csv, time
def build_data():
	
	start_time = time.time()
	'''IMPORTANT VARIABLES'''
	#Data file to use
	csv_file = "On_Time_On_Time_Performance_2015_7.csv"
	#List of the indices of the columns to use as features
	feature_list = [2, 4, 31] #Month(2), Day of Week(4), Listed Departure Time(31)
	#Index of the column to use as a label. 34 for Departure Delay, 45 for Arrival Delay
	label = 34

	#Output data about classifier
	print("--Features (indices):", feature_list)
	print("--Label (indices):", label)

	csvreader = csv.reader(open(csv_file, newline=""))
	print("Loading data from " + csv_file)
	#List of lists that contains x_data (features)
	x = []
	#List that contains y_data (labels)
	y = []
	#Number of flights that had incomplete data
	failed = 0
	delay = 0

	#Convert csvreader to list
	csv_data_list = list(csvreader)
	print("Time to open and convert to list:", time.time()-start_time)

	parse_time = time.time()
	#Turn read object into list, and ignore 1st row that only contains header
	for num, row in enumerate(csv_data_list[1:]):
		#Split row of information by 
		info = str(row).replace("'", "").split(",") #replace("\"", "")

		#Check for delay, if delay, then 1, otherwise 0. Info[39] will be 0 for early or on time
		#This loop also naively trusts that the cell will contain data. This is the lazy way to do this, but if it fails the try, the cell is empty or the wrong data type. It then just excludes this data from the set.
		try:
			#Try to get all data first, then append to the lists at the end if ecerythign is valid
			if float(info[label]) > 0: #39 for Departure, 50 or Arrival
				y_temp = 1
				delay += 1
			else:
				y_temp = 0
			#Add items to features list based on indicies given
			x_temp = [float(info[feat]) for feat in feature_list]
			
			y.append(y_temp)
			#x.append([float(info[2].replace("\"", "")), float(info[4].replace("\"", "")),float(info[36].replace("\"", ""))])
			x.append(x_temp)

		except:
			'''
			print("-------------Failed------------")
			print("Label:", info[label])
			print("Feature:", [info[feat] for feat in feature_list])
			print("-------------------------------")
			'''
			failed += 1
	print("Using", len(x), "data points")
	return [x, y]

# Code source: Gaël Varoquaux
#              Andreas Müller
# Modified for documentation by Jaques Grobler
# License: BSD 3 clause

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis



h = .02  # step size in the mesh
'''
#Original Classifier List
names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Gaussian Process",
		"Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
		"Naive Bayes", "QDA"]

classifiers = [
	KNeighborsClassifier(3),
	SVC(kernel="linear", C=0.025),
	SVC(gamma=2, C=1),
	GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True),
	DecisionTreeClassifier(max_depth=5),
	RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
	MLPClassifier(alpha=1),
	AdaBoostClassifier(),
	GaussianNB(),
	QuadraticDiscriminantAnalysis()]
'''
names = ["Nearest Neighbors", "Decision Tree", "Random Forest", 
		"Neural Net", "AdaBoost", "Naive Bayes", "QDA"]

classifiers = [
	KNeighborsClassifier(14), #3
	DecisionTreeClassifier(max_depth=5),
	RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
	MLPClassifier(alpha=1),
	AdaBoostClassifier(),
	GaussianNB(),
	QuadraticDiscriminantAnalysis()]


X, y = make_classification(n_features=2, n_redundant=0, n_informative=2,
                           random_state=1, n_clusters_per_class=1)
rng = np.random.RandomState(2)
X += 2 * rng.uniform(size=X.shape)
linearly_separable = (X, y)

#Get csv data from file
x, y = build_data()
#[make_moons(noise=0.3, random_state=0), make_circles(noise=0.2, factor=0.5, random_state=1), linearly_separable]
num_iter = 5



output = []
failed = []
print("----Start Model Loop----")
# iterate over classifiers
for name, clf in zip(names, classifiers):
	start_time = time.time()
	print("working:", name)
	avg_list = []
	for i in range(num_iter):
		X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.4)
		try:
			clf.fit(X_train, y_train)
			score = clf.score(X_test, y_test)
			avg_list.append(score)
			#print("Done:", name)
		except:
			print("Failed to run", name)
			failed.append(name)
	print("Done", name)
	output.append([name, sum(avg_list)/float(num_iter), str(time.time()-start_time) + "seconds"])

print("--------Results--------")
[print(x) for x in sorted(output, key=lambda x: x[1])[::-1]]
print("----Failed----")
[print(x) for x in failed]
