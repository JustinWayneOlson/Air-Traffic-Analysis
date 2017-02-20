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
from sklearn.model_selection import train_test_split
#K nearest neighbors (default is 5)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
start_time = time.time()
'''IMPORTANT VARIABLES'''
#Data file to use
csv_file = "On_Time_On_Time_Performance_2015_7.csv"
#Number of iterations to run and average over
num_iter = 10
#Number of neighbors to use in KNeighbors classifier
max_neighbors = 20
#List of the indices of the columns to use as features
feature_list = [2, 4, 31] #Month, Day of Week, Listed Departure Time
#Index of the column to use as a label. 34 for Departure Delay, 45 for Arrival Delay
label = 34

#Output data about classifier
print("--Using from 1 to", max_neighbors, "neighbors for KNeighbors classifier")
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

print("Total size of data set:", len(x))
print("--Number of delays:", delay)
print("--Number of data read failures:", failed)

print("Time to load data:", time.time() - start_time, "seconds")
print("----Testing up to", max_neighbors, "neighbors with", num_iter, "iterations each----")

#List of lists, each nested list is [the number of neighbors used, the accuracy, Time to run all loops, number of loops]
neigh_list = [["Num of Neighbors", "Accuracy", "Time to run", "Num of loops"]]

for num_n in range(1, max_neighbors+1):
	#List to store accuracy and time to split, train, and test each iteration [[accuracy(0.0-1.0), time(seconds)]]
	avg_list = []
	loop_time = time.time()

	for i in range(num_iter):
		#Split data set into 4 sections, x and y training sets, and x and y testing sets
		x_train, x_test, y_train, y_test = train_test_split(x, y) #, test_size = 0.33)

		#Initialize empty classifier
		clf = KNeighborsClassifier(n_neighbors = num_n)
		#Fit data
		clf.fit(x_train, y_train)

		#Test accuracy
		predictions = clf.predict(x_test)
		avg_list.append(accuracy_score(y_test, predictions))

	#print(avg_list)
	neigh_list.append([num_n, sum(avg_list)*100/float(num_iter), time.time()-loop_time, num_iter])
	print("Done with", num_n, "neighbors")

print("----Took", time.time() - start_time, "seconds to test", max_neighbors, "neighbors", num_iter, "times each----")
with open("K_neigh_results_1_to_" + str(max_neighbors) + ".txt", "w") as fo:
	fo.write("Using " + csv_file + " with " + str(len(x)) + " points of data\n")
	fo.write("Features (i ndices): " + str(feature_list)  + "\n")
	fo.write("Label (index): " + str(label) + "\n")
	fo.write("Took " + str(time.time() - start_time) + " seconds to test " + str(max_neighbors) + " neighbors " + str(num_iter) + " times each\n")
	[fo.write(str(i) + "\n") for i in neigh_list]
	fo.write("--------------Sorted--------------\n")
	fo.write(str(neigh_list[0]) + "\n")
	[fo.write(str(i) + "\n") for i in sorted(neigh_list[1:], key=lambda x: x[1])[::-1]]

'''

#Realtime single query of model
while 1:
	inp = input("Query:")
	if (inp == "q"):
		break
	q = inp.split(",")
	q = [float(x) for x in q]
	print(q)
	print(clf.predict([q]))
'''

'''TODO
Make multithreaded (using multiprocess, as threading module shares memory, multiprocessing does not)
'''