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
import csv, time, itertools, threading
from queue import Queue
from sklearn.model_selection import train_test_split
#K nearest neighbors (default is 5)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

'''IMPORTANT VARIABLES'''
#Data file to use
csv_file = "On_Time_On_Time_Performance_2015_7.csv"
#Number of iterations to run and average over
num_iter = 2
#Number of neighbors to use in KNeighbors classifier
num_neighbors = 16
#List of the indices of the columns to use as features
feature_pool = [1,2,3,4,7,10,11,21,31,42,52,56]
#Index of the column to use as a label. 34 for Departure Delay, 45 for Arrival Delay
label = 34
#Number of processes to spawn
max_process = 4
#Minimum length for a combination to be
min_combo = 1
#Maximum length for a combination to be. Range(2,5) creates combinations that range from 2 long to 4 long.
max_combo = 2

#Function that takes in the feature list to analyze using KNeighbors, the csv data, and returns a list with the average accuracy, the number of data points analyzed, and the time it took to run
def kneigh(features):
	start_time = time.time()
	#List of lists that contains x_data (features)
	x = []
	#List that contains y_data (labels)
	y = []
	#Number of flights that had incomplete data
	failed = 0
	delay = 0
	#next(csv_data)
	#Turn read object into list, and ignore 1st row that only contains header
	for row in csv_data_list[1:100000]:
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
			x_temp = [float(info[feat]) for feat in features]		
			y.append(y_temp)
			#x.append([float(info[2].replace("\"", "")), float(info[4].replace("\"", "")),float(info[36].replace("\"", ""))])
			x.append(x_temp)
		except:
			failed += 1

	#List to store accuracy and time to split, train, and test each iteration [[accuracy(0.0-1.0), time(seconds)]]
	avg_list = []
	for i in range(num_iter):
		#Split data set into 4 sections, x and y training sets, and x and y testing sets
		x_train, x_test, y_train, y_test = train_test_split(x, y) #, test_size = 0.33)
		#Initialize empty classifier
		clf = KNeighborsClassifier(n_neighbors = num_neighbors)
		#Fit data
		clf.fit(x_train, y_train)
		#Test accuracy
		predictions = clf.predict(x_test)
		avg_list.append(accuracy_score(y_test, predictions))

	#Return list of [average accuracy, number of data points, and time to run]
	output_queue.put([features, sum(avg_list)*100/float(num_iter), len(x), time.time()-start_time])

#Function to pop feature combination off queue, then call function to analyze the feature set using KNeighbors
def worker():
	while not work_queue.empty():
		item = work_queue.get()
		#print("Working on:", item)
		kneigh(item)
		#print("Done:", item)
		work_queue.task_done()


if __name__ == "__main__":
	prog_start = time.time()
	#Create the Queue to pull feature combinations from
	work_queue = Queue()
	#Create the Queue to put results in
	output_queue = Queue()
	#List of all the possible feature combinations
	combo = []
	#Number of combinations for 12 features: range(1,2) - range(1,13)
	for i in range(min_combo,max_combo):
		combo.extend(list(itertools.combinations(feature_pool, i)))
	#Fill the queue
	[work_queue.put(x) for x in combo]

	#Output data about classifier
	print("--Using", num_neighbors, "neighbors for KNeighbors classifier")
	print("--Label (index):", label)
	print("--Iterations/feature set:", num_iter)
	print("--Testing", len(combo), "combinations, from length", min_combo, "to", max_combo)


	#Open the csv file
	csvreader = csv.reader(open(csv_file, newline=""))
	print("--Loading data from " + csv_file)
	

	#Convert csvreader to list
	csv_data_list = list(csvreader)
	#List of children processes
	children = []
	print("--Spawning", max_process, "children")
	#Spawn Child processes. Off to the races!
	for child in range(max_process):
		#Spawn child with target of worker function. Pass the combination queue, output queue, and list of csv data to worker (Maybe make this shared memory instead?)
		threading.Thread(target=worker).start()

	work_queue.join()
	prog_time = time.time()-prog_start
	print(prog_time, "seconds to test all combinations")
	output = []
	#Print contents of the output queue
	while not output_queue.empty():
		output.append(output_queue.get())

	#Write results to csv file
	with open(str(len(combo)) + "_combos_" + str(num_iter) + "_iters.csv", "w", newline='') as fo:
		writer = csv.writer(fo)
		writer.writerow(["Features", "Accuracy (%)", "Valid Data", "Time (seconds)"])
		#Sort list by second index (accuracy), then reverse to get highest at top
		[writer.writerow(x) for x in sorted(output, key=lambda x: x[1])[::-1]]
		#Write other data about the process
		writer.writerow(["KNeighbors", str(num_neighbors)])
		writer.writerow(["Label Index", str(label)])
		writer.writerow(["Iterations/Feature set", str(num_iter)])
		writer.writerow(["Number of combinations", str(len(combo))])
		writer.writerow(["Feature Pool", str(feature_pool)])
		writer.writerow(["Max Threads", str(max_process)])
		writer.writerow(["Min Combo Length", str(min_combo)])
		writer.writerow(["Max Combo Length", str(max_combo)])
	

	


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