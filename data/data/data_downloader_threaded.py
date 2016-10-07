from urllib.request import urlopen, URLopener #imports urlopen, urlopener
from time import time
import threading
from queue import Queue
# lock to serialize console output
lock = threading.Lock()

#Actual actino function that is performed by each thread
def do_work(item):
	url = "http://tsdata.bts.gov/PREZIP/On_Time_On_Time_Performance_" + str(item[0]) + "_" + str(item[1]) + ".zip"
	#Create object to open url
	website = URLopener()
	file_name = "On_Time_On_Time_Performance_" + str(item[0]) + "_" + str(item[1]) + ".zip"
	#Download file from url and save
	try:
		website.retrieve(url, file_name)
		with lock:
			print("Downloaded:", file_name)
	except: #Error in retrieving website
		with lock:
			print('Website could not be accessed')

# The worker thread pulls an item from the queue and processes it
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

if __name__ == "__main__":
	years = [2015]
	months = [x for x in range(1,13)]

	start = time()
	#Create queue of year, month pairs to download
	q = Queue()
	for year in years:
		for month in months:
			q.put([year,month])

	#Start threads		
	for i in range(4):
	     t = threading.Thread(target=worker)
	     t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
	     t.start()
	q.join()

	print("Downloaded all in", time()-start, "seconds")