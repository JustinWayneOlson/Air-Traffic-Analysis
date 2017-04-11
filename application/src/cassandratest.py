from cassandra.cluster import Cluster
from cassandra.query import dict_factory
import pandas as pd

cluster = Cluster(["localhost"])
session = cluster.connect()
query_string = 'SELECT "Origin", "Dest", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay" FROM AirportTrafficAnalytics.Transtats WHERE "Origin" IN (\'LAS\') AND "Carrier" IN (\'NK\') LIMIT 100 ALLOW FILTERING;'
session.execute("USE AirportTrafficAnalytics")
rows = session.execute(query_string)
cols = ['Origin', "Dest", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay"]
df = pd.DataFrame(columns=cols)
print df
index = 0
while True:
	try:
		row = rows[index]
		df.loc[index] = row
		index += 1
	except IndexError:
		break

print df
