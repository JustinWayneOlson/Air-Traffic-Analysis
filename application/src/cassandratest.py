from cassandra.cluster import Cluster
from cassandra.query import dict_factory
import pandas as pd
import numpy as np

cluster = Cluster(["localhost"])
session = cluster.connect()
#query_string = 'SELECT "Origin", "Dest", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay" FROM AirportTrafficAnalytics.Transtats WHERE "Origin" IN (\'LAS\') AND "Carrier" IN (\'NK\') LIMIT 100 ALLOW FILTERING;'
query_string = 'SELECT "Origin" FROM AirportTrafficAnalytics.Transtats LIMIT 100000 ALLOW FILTERING'
session.execute("USE AirportTrafficAnalytics")
rows = session.execute(query_string)
cols = ['Origin']
#cols = ['Origin', "Dest", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay"]
df = pd.DataFrame(columns=cols)
index = 0
df_index = 0
while True:
   try:
      row = np.array(rows[index])
      if(not((df == row).all(1).any())):
         df.loc[df_index] = row
         df_index += 1
      index += 1
   except IndexError:
      break
print "Done"

print df
