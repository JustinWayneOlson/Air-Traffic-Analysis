import psycopg2

USER='test'
DBNAME='asdf'
PASSWORD='pass'
print "Opening Database Connection"
con = psycopg2.connect('host=localhost dbname={} user={} password={}'.format(DBNAME, USER, PASSWORD))

cursor = con.cursor()
print("Connected")

# #try:
# #    cursor.execute("DROP TABLE test_table CASCADE")
#     con.commit()
# except:
#     pass

cursor.execute("CREATE TABLE test_table ( id      SERIAL PRIMARY KEY, name    TEXT,age     INTEGER);")
con.commit()
con.close()




