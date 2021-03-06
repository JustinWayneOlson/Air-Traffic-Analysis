from cassandra.cluster import Cluster
import csv
import sys
import re
import pprint as pp
import collections

def main(argv):
   field_pattern = re.compile('\"([^\"]*)\"\s([^,]*),')
   end_pattern = re.compile('\/\*End Transtats Table\*\/')
   columns = []
   datatypes = []
   with open('cassandrainit.cql') as init_file:
      for line in init_file:
         match = re.match(field_pattern, line)
         end_match = re.match(end_pattern, line)
         if (end_match):
            break
         elif not(match):
            continue
         else:
            columns.append(match.group(1))
            datatypes.append(match.group(2))
      columns.append('FlightDateString')
      datatypes.append('text')

   csv_file = argv[1]
   cluster = Cluster(["localhost"])
   session = cluster.connect()
   first = True
   with open(csv_file) as csvfile:
      csvdata = csv.reader(csvfile)
      for insert_column in csvdata:
         if(first):
            first = False
            continue
         value_string = ""
         FlightDate = ""
         for index,value in enumerate(insert_column):
            if(columns[index] == 'FlightDate'):
               print("FlightDate")
               column_labels = str(columns).replace("'", '"')[1:-1]
               FlightDate = value
            if datatypes[index] == 'bigint' or datatypes[index] == 'double':
               if value:
                  value_string += '{},'.format(value)
               else:
                  value_string += '0,'
            elif datatypes[index] == 'text':
               value_string += "'{}',".format(value)
            elif datatypes[index] == 'timestamp':
               value_string += "'{}',".format(value)
         value_string += "'{}',".format(str(FlightDate))
         start_string = "INSERT INTO AirportTrafficAnalytics.Transtats({}) VALUES ({});".format(column_labels, value_string[:-1])
         session.execute("USE AirportTrafficAnalytics")
         start_string = start_string.replace('\n', '')
         try:
            print(start_string)
            session.execute(start_string)
         except:
            print "Invalid CSV Format"
if __name__ == "__main__":
   main(sys.argv)

