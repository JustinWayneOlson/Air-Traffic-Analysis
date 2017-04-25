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
csv_file = "On_Time_On_Time_Performance_2015_7.csv"
#Number of iterations to run and average over
num_iter = 2
#Alpha value for MLPClassifier. 
#1st run: [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50, 100, 500]
#2nd run: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1]
#3rd run: [0.005, 0.01, 0.05, 0.1, 0.5, 1, 10]
#4th run: [0.005, 0.01, 0.1, 1]
alpha_value = [0.005, 0.01, 0.1, 1]
#Composition of hidden layers for MLPClassifier (100,40,) Would be 2 layers, with 100 nodes in the first layer and 40 nodes in the second
#2 layer with 5000 layer take too long[(20,10,5,), (20,10,), (50,25,), (100,50,), (500, 100,), (1000, 500,), (5000, 1000,), (5000, 2500,), (20,), (50,), (100,), (500,), (1000,), (5000,), (10000,), (20000,), (50000,)]#(100,50)#(20,10,5,)
#1st run: [(20,10,5,), (20,10,), (50,25,), (100,50,), (500, 100,), (20,), (50,), (100,), (500,)]
#2nd run: [(500,), (500,100,), (1000,), (1000, 100,), (1000, 200,), (1000, 500,)]
#3rd run: [(500,100,), (1000,), (1000, 100,), (1000, 200,), (2000)]
#4th run: [(500,100,), (1000,), (1000, 200,), (2000,)]
#5th run: [(500,100,), (1000,), (1000, 200,)]
hidden_layer_comp = [(500,100,), (1000,), (1000, 200,)]
total_combos = len(hidden_layer_comp)*len(alpha_value)
#Granulatity to round to
#1st Rounds: 30
#2nd run: 20
round_base = 20 #Will be off by round_base/2 at most. Ex. With round_base=20, 11 rounds to 20, 10 rounds to 0
#List of the indices of the columns to use as features
feature_list = [2,4,31,56]#[2,4,11,21,31,56] #Month(2), Day of Week(4), Listed Departure Time(31) #10,31 late additions
#Index of the column to use as a label. 34 for Departure Delay, 45 for Arrival Delay
label = 54 #53 for total time of the flight, 54 for only time in the air

#Output data about classifier
print("--Alpha Values to test:", len(alpha_value))
print("--Layer compositioms to test:", len(hidden_layer_comp))
print("--Total combinations:", total_combos)
print("--Features (indices):", feature_list)
print("--Label (indices):", label)
print("--Iterations per combination:", num_iter)


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
for num, row in enumerate(csv_data_list[1:300000]): #[1:300000]
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
		failed += 1

print("----------Time to parse data into lists:", time.time()-parse_time)

print("Total size of data set:", len(x))
print("--Number of data read failures:", failed)

print("Time to load data:", time.time() - start_time, "seconds")

from sklearn.model_selection import train_test_split
#K nearest neighbors (default is 5)
from sklearn.neural_network import MLPClassifier

#List to store all results from all combinations of testing. [alpha, layer comp, accuracy, time/loop]
mlp_list = []
cur_combo = 0
#Iterate through alpha values
for loop_alpha in alpha_value:
	#Loop through hidden layer compositions
	for loop_layer in hidden_layer_comp:
		#List to store accuracy and time to split, train, and test each iteration [[accuracy(0.0-1.0), time(seconds)]]
		avg_list = []
		for i in range(num_iter):
			loop_time = time.time()
			#Split data set into 4 sections, x and y training sets, and x and y testing sets
			x_train, x_test, y_train, y_test = train_test_split(x, y) #, test_size = 0.33)
			
			#Initialize empty classifier
			clf = MLPClassifier(alpha=loop_alpha, hidden_layer_sizes=loop_layer)
			#train_time = time.time()
			#Fit data
			clf.fit(x_train, y_train)
			#print("Time to train", time.time()-train_time)
			#Test accuracy
			avg_list.append([clf.score(x_test, y_test), time.time() - loop_time])

		#Split list of lists into separate list
		accs, times = zip(*avg_list)
		#Add to list of overall results
		mlp_list.append([loop_alpha, loop_layer, sum(accs)*100/float(num_iter), sum(times)/float(num_iter)])
		'''
		print("Average accuracy")
		print(sum(accs)*100/float(num_iter), "%")
		print("Average time per loop")
		print(sum(times)/float(num_iter), "seconds")
		'''
		cur_combo += 1
		print("--Percent Done:", 100*(cur_combo/total_combos), "| Alpha:", loop_alpha, "| Layer:", loop_layer)
	print("Alpha", loop_alpha, "| Percent Done:", 100*(cur_combo/total_combos), "| Time:", time.time()-start_time)


prog_time = time.time()-start_time
print("----Took", prog_time, "seconds to test", len(hidden_layer_comp)*len(alpha_value), "combos", num_iter, "times each----")

#Write results to csv file
with open("MLP_" + str(len(alpha_value)) + "_alphas_" + str(len(hidden_layer_comp)) + "_layers_" + str(total_combos) + "_combos_" + str(num_iter) + "_iters.csv", "w", newline='') as fo:
	writer = csv.writer(fo)
	#Write data about the process
	writer.writerow(["Feature Indices", str(feature_list)])
	writer.writerow(["Label Index", str(label)])
	writer.writerow(["Iterations/Feature set", str(num_iter)])
	writer.writerow(["Number of combinations", str(total_combos)])
	writer.writerow(["Rounding Base", str(round_base)])
	writer.writerow(["Alpha Values", str(alpha_value)])
	writer.writerow(["Hidden Layer Comps", str(hidden_layer_comp)])
	#writer.writerow(["Feature Pool", str(feature_pool)])
	#writer.writerow(["Max Threads", str(max_process)])
	#writer.writerow(["Min Combo Length", str(min_combo)])
	#writer.writerow(["Max Combo Length", str(max_combo)])
	writer.writerow(["Time to Run (Sec)", str(prog_time)])
	writer.writerow(["CSV Input File Name", csv_file])
	writer.writerow(["Valid Data", str(len(x))])
	writer.writerow(["Alpha Value", "Hidden Layer Comp", "Accuracy (%)", "Time/Loop (seconds)"])
	#Sort list by third column (accuracy), then reverse to get highest at top
	[writer.writerow(x) for x in sorted(mlp_list, key=lambda x: x[2])[::-1]]
	
