from cassandra.cluster import Cluster
import csv
import sys
import re
import pprint as pp
import collections

def main(argv):
   field_pattern = re.compile('\"([^\"]*)\"\s([^,]*),')
   columns = []
   datatypes = []
   with open('cassandrainit.cql') as init_file:
      for line in init_file:
         match = re.match(field_pattern, line)
         if not(match):
            continue
         else:
            columns.append(match.group(1))
            datatypes.append(match.group(2))

   csv_file = argv[1]
   cluster = Cluster(["localhost"])
   session = cluster.connect()
   first = True
   column_labels = str(columns).replace("'", '"')[1:-1]
   with open(csv_file) as csvfile:
      csvdata = csv.reader(csvfile)
      for insert_column in csvdata:
         if(first):
            first = False
            continue
         value_string = ""
         for index,value in enumerate(insert_column):
            if datatypes[index] == 'bigint' or datatypes[index] == 'double':
               if value:
                  value_string += '{},'.format(value)
               else:
                  value_string += 'null,'
            elif datatypes[index] == 'text':
               value_string += "'{}',".format(value)
            elif datatypes[index] == 'timestamp':
               value_string += "'{}',".format(value)
         start_string = "INSERT INTO AirportTrafficAnalytics.Transtats({}) VALUES ({});".format(column_labels, value_string[:-1])
         session.execute("USE AirportTrafficAnalytics")
         session.execute(start_string)
if __name__ == "__main__":
   main(sys.argv)

