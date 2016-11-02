import csv
#File to import data from .dat file to .csv file. On;y writes airports in the USA with 3 letter codes
with open("airport_locations.dat", "r", encoding="utf8") as airports_in:
	#Create csv file
	with open("airport_locations_out.csv", "w", newline="") as airports_out:
		#Set up the writer for the csv file
		file_writer = csv.writer(airports_out, delimiter=",")
		#Write the first row hat tells the user what each column means
		file_writer.writerow(["City", "Airport", "Lat", "Lon"])
		#Iterate through the data file
		for line in airports_in:
			#Try, except in case decoder encounter weird character. Outputs the openflights airport id if it fails
			try:
				data = line.split(",")
				#Filter out only airports in the USA and with 3 letter codes
				if ((data[3].replace("\"", "") == "United States") and (len(data[4].replace("\"", "")) > 1)):
					file_writer.writerow([(data[2] + ", " + data[3]).replace("\"", ""), (data[4]).replace("\"", ""), data[6], data[7]])
				'''
				print("City:", data[2], "Country:", data[3], "3 Letter:", data[4])
				print("Lat:", data[6], "Long:", data[7])
				'''
			#Print openflights airport id if writing to csv fails
			except:
				print("Could not import airport num:", data[0])
