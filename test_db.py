# DATABASE TESTING via SQLITE3
import csv
import sqlite3

# connect to database
connection = sqlite3.connect('test.db')
# database cursor used to executive sql statements and fetch results
#   from sql queries
cursor = connection.cursor()

# creating a test table
create_table = "CREATE TABLE test_table(" \
               "id INTEGER PRIMARY KEY AUTOINCREMENT," \
               "Column1 TEXT NOT NULL, " \
               "Column2 TEXT NOT NULL);"

# putting the test table into our db
cursor.execute(create_table)

# open csv file we want to ingest into our db -> test.db
file = open('test.csv')

# reading contents of csv
contents = csv.reader(file)

# sql query to insert data from csv into test table
insert_records = "INSERT INTO test_table " \
                 "(Column1, Column2) " \
                 "VALUES(?,?)"

# importing contents of csv into test_only table
cursor.executemany(insert_records, contents)

# sql query retrieving all data from test_only table
#   to verify that the data from the cvs was successfully
#   inserted into the aforementioned table
select_all = "SELECT * FROM test_table"
rows = cursor.execute(select_all).fetchall()

# print to console
for r in rows:
    print(r)

# commit changes
connection.commit()

# close the db connection
connection.close()
