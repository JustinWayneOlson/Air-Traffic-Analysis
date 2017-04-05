from cassandra.cluster import Cluster

cluster = Cluster(["localhost"])
session = cluster.connect()
query_string = 'SELECT "Origin", "Dest", "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay" FROM AirportTrafficAnalytics.Transtats WHERE "Origin" IN (\'LAS\') AND "Carrier" IN (\'NK\') LIMIT 100 ALLOW FILTERING;'
session.execute("USE AirportTrafficAnalytics")
rows = session.execute(query_string);
for row in rows:
   print row
