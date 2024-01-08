import sqlite3

#Connecting to sqlite
connection = sqlite3.connect('test.db')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping EMPLOYEE table if already exists
cursor.execute("DROP TABLE test_table")
print("Table dropped... ")

#Commit your changes in the database
connection.commit()

#Closing the connection
connection.close()