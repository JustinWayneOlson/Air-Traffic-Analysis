from urllib.request import urlopen, URLopener #imports urlopen, urlopener
from time import time


if __name__ == "__main__":
	years = [2015]
	months = [x for x in range(1,13)]

	start = time()
	#Iterate through years and months
	for cur_year in years:
		for cur_month in months:
			url = "http://tsdata.bts.gov/PREZIP/On_Time_On_Time_Performance_" + str(cur_year) + "_" + str(cur_month) + ".zip"
			#Create object to open url
			website = URLopener()
			file_name = "On_Time_On_Time_Performance_" + str(cur_year) + "_" + str(cur_month) + ".zip"
			#Download file from url and save
			try:
				website.retrieve(url, file_name)
				print("Downloaded:", file_name)
			except: #Error in retrieving website
				print('Website could not be accessed')

	print("Downloaded all in", time()-start, "seconds")