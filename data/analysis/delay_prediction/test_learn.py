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
csv_file = "On_Time_On_Time_Performance_2015_1.csv"#"sample.csv"
csvreader = csv.reader(open(csv_file, newline=""))
print("Using " + csv_file)
#List of lists that contains x_data (features)
x = []
#List that contains y_data (labels)
y = []
#Number of flights that had incomplete data
failed = 0
#Turn read object into list, and ignore 1st row that only contains headers
for num, row in enumerate(list(csvreader)[1:]):
	#Split row of information by 
	info = str(row).split(",")
	'''
	print(info[67])
	print("-----------")
	'''
	
	#Check for delay, if delay, then 1, otherwise 0. Info[39] will be 0 for early or on time
	#This loop also naively trusts that the cell will contain data. This is the lazy way to do this, but if it fails the try, the cell is empty or the wrong data type. It then just excludes this data from the set.
	try:
		if float(info[39]) > 0: #39 for Departure, 50 or Arrival
			y.append(1)
		else:
			y.append(0)
		#Add item to features list
		x.append([float(info[2].replace("\"", "")), float(info[4].replace("\"", "")),float(info[36].replace("\"", ""))])
	except:
		#print("Failed on row:", num)
		failed += 1

'''
print("Num of features:", len(x))
print("Num of labels:", len(y))
'''

print("----Time to load data:", time.time() - start_time, "seconds----")
from sklearn.model_selection import train_test_split
#Split data set into 4 sections, x and y training sets, and x and y testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y) #, test_size = 0.33)
print("Size of Training Set:", len(x_train))
print("Size of Testing Set:", len(x_test))
#Pick classifier

#K nearest neighbors (default is 5)
from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors = 10)

#Fit data
clf.fit(x_train, y_train)

print("----Departure delay analysis----")
#Test accuracy
predictions = clf.predict(x_test)
end_time = time.time() - start_time
print("Took", end_time, "seconds for", len(x), "flights")
from sklearn.metrics import accuracy_score
print(str(accuracy_score(y_test, predictions)*100) + "% accurate predictions")

'''TODO
Loop tests to get averages, don;t reload data every time
Use non binary delay methods, and see if you can predict how the delay will be
Train model using one month of data, then test using another month
Test different features and test arrival times
'''