from cassandra.cluster import Cluster

cluster = Cluster(["localhost"])
session = cluster.connect()
session.execute("""CREATE KEYSPACE IF NOT EXISTS AirportTrafficAnalytics WITH replication = { 'class' : 'SimpleStrategy',
'replication_factor' : '2' } AND durable_writes = true;""")
session.execute("USE AirportTrafficAnalytics")
session.execute("""CREATE TABLE MLPClassifier, (
   "Year" bigint,
   "Month" bigint,
   "RoundingBase" bigint,
   "Features" list<int>,
   "Label" bigint,
   "HLayer" list<int>,
   "Alpha" double,
   "RowsTrain" bigint,
   "Accuracy" double,
   "Model" blob,
   PRIMARY KEY ("Year", "Month", "RoundingBase", "Features", "Label", "HLayer", "Alpha"),
) WITH CLUSTERING ORDER BY ("Year" DESC);""")