#Mitch Zinser
#Python 3.5
#Script that trains some usually accurate models and stores the data in Cassandra
import MLP_Class, time

if __name__ == "__main__":
	#Number of rows to read in from csv files
	row_num = 50000#0
	#Configurations that have worked well generally. (0.005 | 500,100), (0.1 | 500,100), (0.005 | 2000), (0.01 | 500), (0.01 | 2000)
	#Configurations to pickle. Format is [(year, month, alpha, h layer)]
	y = 2015
	month_list = [i for i in range(1,13)]
	config_list = [[0.005,[500,100]], [0.005,[2000]], [0.01,[500]], [0.01,[2000]], [0.1,[500,100]]]
	#Granulatity to round to
	round_base = 20 #Will be off by round_base/2 at most. Ex. With round_base=20, 11 rounds to 20, 10 rounds to 0
	

	use_cassandra = True
	if use_cassandra:
		#List of the cassandra columns to use as features
		feature_list = ['Month', 'DayOfWeek', 'CRSDepTime', 'Distance']
		#Index of the column to use as a label
		label = 'AirTime'
		
	else:
		#List of the indices of the columns to use as features
		feature_list = [2,4,31,56]
		#Index of the column to use as a label
		label = 54#54 #53 for total time of the flight, 54 for only time in the air
		
	
	#Loop over months and configurations and train a model. If the accuracy is under 50%, don't save the model
	for month in month_list:
		for config in config_list:
			alpha = config[0]
			layer = config[1]
			print("--------")
			try:
				start_time = time.time()
				#Create object
				test_mlp = MLP_Class.MLP(y,month,row_num,feature_list,label,round_base,alpha,layer)
				#Test if the model is already in the database
				if test_mlp.check_database():
					print("Model already in Cassandra")
				#Otherwise train and save a model
				else:
					#Read in data
					if use_cassandra:
						#Read in data from Cassandra
						test_mlp.read_database()
					else:
						#Read in data from csv file
						test_mlp.read_csv()
					#Train classifier, continue if training successful
					#print("Training")
					if test_mlp.train():
						#Write model to Cassandra if accuracy is over 50%
						if test_mlp.get_accuracy() > 50.0:
							if test_mlp.save():
								print("Saved to Cassandra")
							else:
								print("Error Saving to Cassandra")
							'''
							print("CHECKING DB")
							print(test_mlp.check_database())
							print("Loading:", test_mlp.load())
							print("New accuracy:", test_mlp.test_accuracy())
							'''
						else:
							print("Not saved to Cassandra, accuracy too low")
						
						print("Trained in", time.time()-start_time, "seconds")
						print("Month:", month, "| Config:", config, "| Accuracy:", test_mlp.get_accuracy())
						

					else:
						print("Failed to train")


			except:
				print("----Problem training----")
				print("Month:", month, "| Config:", config)
				