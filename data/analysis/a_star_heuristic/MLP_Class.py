#Mitch Zinser
#Class that allows easy creation, training, and persisting of MLP Classifiers
#Uses csv to import data from csv files, uses
import csv
#Automatically splits the data into training and testing sets
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

#Class that creates MLP Classifier, reads data, trains the classifier, writes the classifier to disk
class MLP:
	'''Required class contructor parameters:
	year: year to get data from
	month: month to get data from
	rows: number of data points to read in
	features: list of features to get
	label: single label to estimate
	rounding: Base to round numbers read in to
	alpha: alpha value to use
	h_layer: hidden layer composition, list of ints that describe composition of each hidden layer
	'''
	def __init__(self, year, month, rows, features, label, rounding, alpha, h_layer):
		self.year = year
		self.month = month
		self.rows = rows
		self.features = features
		self.label = label
		self.rounding = rounding
		self.alpha = alpha
		self.h_layer = h_layer
		#Store data that has been read in in the object
		self.x = []
		self.y = []
		#Store the MLPClassifier object
		self.classifier = MLPClassifier(alpha=self.alpha, hidden_layer_sizes=self.h_layer)
		#Store the accuracy of the model
		self.accuracy = 0

	#Read data in from a csv file. Returns the number of data points that could be read successfully
	def read_csv(self):
		filename = "On_Time_On_Time_Performance_" + str(self.year) + "_" + str(self.month) + ".csv"
		csvreader = csv.reader(open(filename, newline=""))
		print("Loading data from " + filename)
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
		for num, row in enumerate(csv_data_list[1:self.rows]): #[1:300000]
			#Split row of information by 
			info = str(row).replace("'", "").split(",") #replace("\"", "")

			#Check for delay, if delay, then 1, otherwise 0. Info[39] will be 0 for early or on time
			#This loop also naively trusts that the cell will contain data. This is the lazy way to do this, but if it fails the try, the cell is empty or the wrong data type. It then just excludes this data from the set.
			try:
				#Try to get all data first, then append to the lists at the end if ecerythign is valid
				if float(info[self.label]) > 0: #39 for Departure, 50 or Arrival
					y_temp = int(self.rounding * round(float(info[self.label])/self.rounding)) #Round to nearest 5
				else:
					y_temp = 0
				#Add items to features list based on indicies given
				x_temp = [float(info[feat]) for feat in self.features]
				
				y.append(y_temp)
				#x.append([float(info[2].replace("\"", "")), float(info[4].replace("\"", "")),float(info[36].replace("\"", ""))])
				x.append(x_temp)

			except:
				failed += 1
		#Store created lists of data in the private variables
		self.x = x
		self.y = y
		#Return the number of data points that could be read successfully
		return len(x)

	#Read data in from the cassandra database. Returns the number of data points that could be successfully read
	def read_database(self):
		#TODO
		pass

	#Train the model and record it's accuracy. Checks if data has been read in before training. Returns True if training succeeded, False if training failed.
	def train(self):
		#Check if there is data already read in, and if the lengths of the feature and label sets are the same
		if ((len(self.x) == len(self.y)) && (len(self.x) != 0)):
			#Split data set into 4 sections, x and y training sets, and x and y testing sets
			x_train, x_test, y_train, y_test = train_test_split(self.x, self.y) #, test_size = 0.33)
			#Fit data
			self.classifier.fit(x_train, y_train)
			self.accuracy = self.classifier.score(x_test, y_test)
			return True
		else:
			return False

	#Getter that returns the % accuracy of the currently trained model.
	def get_accuracy(self):
		return self.accuracy*100
'''
start_time = time.time()
'''IMPORTANT VARIABLES'''
#Data file to use
#csv_file = "On_Time_On_Time_Performance_2015_7.csv"
#Number of iterations to run and average over
num_iter = 2
#Number of rows to read in from csv files
row_num = 400000
'''
alpha_value = [0.005, 0.01, 0.1, 1]
#Composition of hidden layers for MLPClassifier (100,40,) Would be 2 layers, with 100 nodes in the first layer and 40 nodes in the second
hidden_layer_comp = [(500,100,), (1000,), (1000, 200,)]
'''
#Configurations that have worked well generally. (0.005 | 500,100), (0.1 | 500,100), (0.005 | 2000), (0.01 | 500), (0.01 | 2000)
#Configurations to pickle. Format is [(year, month, alpha, h layer)]
mlp_configs = [(2015, 1, 0.01, (500,100))]
total_combos = len(mlp_configs)
#Granulatity to round to
#1st Rounds: 30
#2nd run: 20
round_base = 20 #Will be off by round_base/2 at most. Ex. With round_base=20, 11 rounds to 20, 10 rounds to 0
#List of the indices of the columns to use as features
feature_list = [2,4,31,56]#[2,4,11,21,31,56] #Month(2), Day of Week(4), Listed Departure Time(31) #10,31 late additions
#Index of the column to use as a label. 34 for Departure Delay, 45 for Arrival Delay
label = 54 #53 for total time of the flight, 54 for only time in the air

#Output data about classifier
print("--Total combinations:", total_combos)
print("--Features (indices):", feature_list)
print("--Label (indices):", label)
print("--Iterations per combination:", num_iter)


#List to store most accurate trained classifier [(accuracy, mlp classifier)]
mlp_list = []
cur_combo = 0
#Iterate through months
for loop_mlp in mlp_configs:
	#Load data for this month
	x,y = read_csv(loop_mlp[0], loop_mlp[1], row_num)

	#List to store accuracy and Classifier model [[accuracy, Trained Classifier, (config)]]
	avg_list = []

	for i in range(num_iter):
		loop_time = time.time()
		#Split data set into 4 sections, x and y training sets, and x and y testing sets
		x_train, x_test, y_train, y_test = train_test_split(x, y) #, test_size = 0.33)
		#Initialize empty classifier
		clf = MLPClassifier(alpha=loop_mlp[2], hidden_layer_sizes=loop_mlp[3])
		#train_time = time.time()
		#Fit data
		clf.fit(x_train, y_train)
		#print("Time to train", time.time()-train_time)
		#Test accuracy
		avg_list.append([clf.score(x_test, y_test), clf])

	#Get max accuracy model of this configuration
	mlp_list.append([max(avg_list), loop_mlp])
	'''
	#Split list of lists into separate list
	accs, times = zip(*avg_list)
	#Add to list of overall results
	mlp_list.append([loop_month, loop_mlp[0], loop_mlp[1], sum(accs)*100/float(num_iter), sum(times)/float(num_iter)])
	'''
	cur_combo += 1
	print("--Percent Done:", 100*(cur_combo/total_combos), "| Year:", loop_mlp[0], "| Month:", loop_mlp[1], "| Alpha:", loop_mlp[2], "| Layer:", loop_mlp[3])


prog_time = time.time()-start_time
print("----Took", prog_time, "seconds to test", total_combos, "combos", num_iter, "times each----")
import pickle
#Pickle or persist the models to the database. dump writes to file, dumps just creates a string of bytes
for i in mlp_list:
	#Write to file or database
	print("----Pickling----")
	filename = "f:" + str(feature_list) + "_l:" + str(label) + "_r:" + str(round_base) + "_a:" + str(i[0][0]) + "_c:" + str(i[1]) + ".pkl"
	with open(filename, "wb") as output_file:
		pickle.dump(clf, output_file, pickle.HIGHEST_PROTOCOL)

'''

'''
#Write results to csv file
with open("MLP_" + str(len(csv_inputs)) + "_months_" + str(len(mlp_configs)) + "_configs_" + str(total_combos) + "_combos_"+ str(num_iter) + "_iters.csv", "w", newline='') as fo:
	writer = csv.writer(fo)
	#Write data about the process
	writer.writerow(["Feature Indices", str(feature_list)])
	writer.writerow(["Label Index", str(label)])
	writer.writerow(["Iterations/Feature set", str(num_iter)])
	writer.writerow(["Number of combinations", str(total_combos)])
	writer.writerow(["Rounding Base", str(round_base)])
	writer.writerow(["Months Tested", str(csv_inputs)])
	writer.writerow(["MLP Configs", str(mlp_configs)])
	#writer.writerow(["Feature Pool", str(feature_pool)])
	#writer.writerow(["Max Threads", str(max_process)])
	#writer.writerow(["Min Combo Length", str(min_combo)])
	#writer.writerow(["Max Combo Length", str(max_combo)])
	writer.writerow(["Time to Run (Sec)", str(prog_time)])
	writer.writerow(["Valid Data", str(len(x))])
	writer.writerow(["Month", "Alpha Value", "Hidden Layer Comp", "Accuracy (%)", "Time/Loop (seconds)"])
	#Sort list by third column (accuracy), then reverse to get highest at top
	[writer.writerow(x) for x in sorted(mlp_list, key=lambda x: x[3])[::-1]]
	
'''



'''
with open("2015_07_data=" + str(len(x)) + "_feat=" + str(feature_list) + "_label=" + str(label) + "_round=" + str(round_base) + "_alpha=" + str(alpha_value) + "_layer_comp=" + str(hidden_layer_comp) + ".pkl", "wb") as output_file:
	pickle.dump(clf, output_file, pickle.HIGHEST_PROTOCOL)
'''
'''
print("----Pickling with 3.0 Protocol----")
with open("pkl3_2015_07_alpha=" + str(alpha_value) + "layer_comp=" + str(hidden_layer_comp) + ".pkl", "wb") as output_file:
	pickle.dump(clf, output_file, pickle.DEFAULT_PROTOCOL)
'''