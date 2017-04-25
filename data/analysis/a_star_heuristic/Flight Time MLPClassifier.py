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
start_time = time.time()
'''IMPORTANT VARIABLES'''
#Data file to use
csv_file = "On_Time_On_Time_Performance_2015_4.csv"
#Number of iterations to run and average over
num_iter = 1
#Alpha value for MLPClassifier. 
alpha_value = 0.1 #0.1 -> ~65%, 1.0 -> ~60%
#Composition of hidden layers for MLPClassifier (100,40,) Would be 2 layers, with 100 nodes in the first layer and 40 nodes in the second
layers = (500,100,)
hidden_layer_comp = layers#(100,50)#(20,10,5,)
#Granulatity to round to
round_base = 20 #Will be off by round_base/2 at most. Ex. With round_base=20, 11 rounds to 20, 10 rounds to 0
#List of the indices of the columns to use as features
#Test 6,7
feature_list = [2,4,31,56]#[2,4,11,21,31,56] #Month(2), Day of Week(4), Listed Departure Time(31) #10,31 late additions
#Index of the column to use as a label. 34 for Departure Delay, 45 for Arrival Delay
label = 54 #53 for total time of the flight, 54 for only time in the air

#Output data about classifier
print("--Alpha Value", alpha_value)
print("--Hidden Layer Comp", hidden_layer_comp)
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
print("----------Time to open and convert to list:", time.time()-start_time)

parse_time = time.time()
#Turn read object into list, and ignore 1st row that only contains header
for num, row in enumerate(csv_data_list[1:300000]):
	#Split row of information by 
	info = str(row).replace("'", "").split(",") #replace("\"", "")
	#Check for delay, if delay, then 1, otherwise 0. Info[39] will be 0 for early or on time
	#This loop also naively trusts that the cell will contain data. This is the lazy way to do this, but if it fails the try, the cell is empty or the wrong data type. It then just excludes this data from the set.
	try:
		#Try to get all data first, then append to the lists at the end if ecerythign is valid
		if float(info[label]) > 0: #39 for Departure, 50 or Arrival
			y_temp = int(round_base * round(float(info[label])/round_base)) #Round to nearest 5
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
print("----------Time to parse data into lists:", time.time()-parse_time)

print("Total size of data set:", len(x))
print("--Number of data read failures:", failed)

print("Time to load and parse data:", time.time() - start_time, "seconds")
print("----Testing", num_iter, "iterations starting at ", time.ctime(), "----")
from sklearn.model_selection import train_test_split
#K nearest neighbors (default is 5)
from sklearn.neural_network import MLPClassifier

#List to store accuracy and time to split, train, and test each iteration [[accuracy(0.0-1.0), time(seconds)]]
avg_list = []

for i in range(num_iter):
	loop_time = time.time()
	#Split data set into 4 sections, x and y training sets, and x and y testing sets
	x_train, x_test, y_train, y_test = train_test_split(x, y) #, test_size = 0.33)
	
	#Initialize empty classifier
	clf = MLPClassifier(alpha=alpha_value, hidden_layer_sizes=hidden_layer_comp)
	train_time = time.time()
	#Fit data
	clf.fit(x_train, y_train)
	print("Time to train", time.time()-train_time)
	#Test accuracy
	
	'''
	#Slower(?) predict
	predictions = clf.predict(x_test)
	#Test against random guessing
	import random
	from sklearn.metrics import accuracy_score
	predictions = [int(round_base * round(float(random.randint(0,660))/round_base)) for x in range(len(y_test))]
	avg_list.append([accuracy_score(y_test, predictions), time.time() - loop_time])
	'''
	pred_score = 0
	preds = clf.predict(x_test)
	

	for ind,t in enumerate(preds):
		if int(round_base * round(float(t)/round_base)) == y_test[ind]:
			pred_score += 1

	avg_list.append([float(pred_score)/len(x_test), time.time() - loop_time])

	#avg_list.append([clf.score(x_test, y_test), time.time() - loop_time])

#print(avg_list)
print("----Took", time.time() - start_time, "seconds to test", num_iter, "times----")
#Split list of lists into separate list
accs, times = zip(*avg_list)
print("Average accuracy")
print(sum(accs)*100/float(num_iter), "%")
print("Average time per loop")
print(sum(times)/float(num_iter), "seconds")


import pickle
print("----Pickling----")
with open("Tester04.pkl", "wb") as output_file:
	pickle.dump(clf, output_file, pickle.HIGHEST_PROTOCOL)
'''
with open("2015_07_data=" + str(len(x)) + "_feat=" + str(feature_list) + "_label=" + str(label) + "_round=" + str(round_base) + "_alpha=" + str(alpha_value) + "_layer_comp=" + str(hidden_layer_comp) + ".pkl", "wb") as output_file:
	pickle.dump(clf, output_file, pickle.HIGHEST_PROTOCOL)
'''
'''
print("----Pickling with 3.0 Protocol----")
with open("pkl3_2015_07_alpha=" + str(alpha_value) + "layer_comp=" + str(hidden_layer_comp) + ".pkl", "wb") as output_file:
	pickle.dump(clf, output_file, pickle.DEFAULT_PROTOCOL)
'''


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