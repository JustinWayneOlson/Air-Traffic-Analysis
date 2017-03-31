#Mitch Zinser
#Python 3.5
#Class that allows easy creation, training, and persisting of MLP Classifiers
#Uses csv to import data from csv files, import pickle to persist classifier object
import csv, pickle
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
		##print("Loading data from " + filename)
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
		if ((len(self.x) == len(self.y)) and (len(self.x) != 0)):
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
	#Get the pickled classifier
	def pickle_classifier(self):
		return pickle.dumps(clf, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
	import time
	start_time = time.time()
	'''IMPORTANT VARIABLES'''
	#Number of rows to read in from csv files
	row_num = 200000
	#Configurations that have worked well generally. (0.005 | 500,100), (0.1 | 500,100), (0.005 | 2000), (0.01 | 500), (0.01 | 2000)
	#Configurations to pickle. Format is [(year, month, alpha, h layer)]
	y = 2015
	m = 1
	alpha = 0.1
	layer = (500,100)
	#Granulatity to round to
	round_base = 20 #Will be off by round_base/2 at most. Ex. With round_base=20, 11 rounds to 20, 10 rounds to 0
	#List of the indices of the columns to use as features
	feature_list = [2,4,31,56]#[2,4,11,21,31,56] #Month(2), Day of Week(4), Listed Departure Time(31) #10,31 late additions
	#Index of the column to use as a label. 34 for Departure Delay, 45 for Arrival Delay
	label = 54 #53 for total time of the flight, 54 for only time in the air
	#Create object
	test_mlp = MLP(y,m,row_num,feature_list,label,round_base,alpha,layer)
	#Read in data
	print("Reading in data from csv")
	print(test_mlp.read_csv())
	#Train classifier
	print("Training")
	print(test_mlp.train())
	print("Accurcy")
	print(test_mlp.get_accuracy())

	prog_time = time.time()-start_time
	print("Ran in", prog_time, "seconds")
