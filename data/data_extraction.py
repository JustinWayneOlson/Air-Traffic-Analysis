#Python script to take in excel data, input into Pandas dataframe,
#and create a SQL table based on that dataframe

from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import sys

#Format: posgtgresql://[username]:[password]@[host]:[port]/[database name]
POSTGRES_URL = "postgresql://test:pass@localhost:5432/test"

def main(argv):
	csv_files = argv[1:]
	for file in csv_files:
		#Create pandas dataframe from CSV file
		dataframe = pd.DataFrame.from_csv(file)

		#Connect to Postgres database
		engine = create_engine(POSTGRES_URL)

		#Create a tabled called "airplanez" at populate with dataframe values
		dataframe.to_sql('airplanez', engine)

if __name__ == "__main__":
	main(sys.argv)