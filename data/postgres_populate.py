import psycopg2
import csv
import sys
import re

def main(argv):
   con = psycopg2.connect(host="localhost", database="airports", user="postgres", password="postgres")
   cur = con.cursor()

   csvObject = csv.reader(open(argv[1]), dialect = 'excel', delimiter = ',');
   pattern = re.compile('.*"(\w*)"\s((?:\w\s*)*).*')
   header_string = None
   headers = []

   schema = {}
   with open('schema.psql') as infile:
      for line in infile:
         if(re.match(pattern, line)):
            schema[re.match(pattern, line).group(1)] = re.match(pattern, line).group(2)


   for row in csvObject:
      if header_string is None:
         row = row[:-1]
         headers = row
         header_string = str(headers).replace('[','(').replace(']',')').replace("'", '"'); #Format for psql query
         #values_string = str(['%s' for x in range(0, len(row))]).replace(']',')').replace('[','(').replace("'",'')
      else:
         value_string = ""
         for index,value in enumerate(row):
            if(index == len(headers)):
               break
            if(schema[headers[index]] == 'bigint' or schema[headers[index]] == 'double precision'):
               if(value):
                  value_string += "{},".format(value.replace(',',''))
               else:
                  value_string += "{},".format(0)
            elif(schema[headers[index]] == 'text'):
               if(value):
                  value_string += "'{}',".format(value.replace(',',''))
               else:
                  value_string += "'{}',".format('')
            else:
               print schema[headers[index]]
         value_string = value_string[:-1]
         #values_string = str(row[:-1]).replace('[','(').replace(']',')'); #Format for psql query
         insert_string = "INSERT INTO flights {} VALUES ({});".format(header_string, value_string)
         cur.execute(insert_string)
         con.commit()


if __name__ == '__main__':
   main(sys.argv)

