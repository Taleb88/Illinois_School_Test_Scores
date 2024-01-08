import sqlite3

#Connecting to sqlite
connection = sqlite3.connect('student.db')

#Creating a cursor object using the cursor() method
cursor = connection.cursor()

#Doping EMPLOYEE table if already exists
cursor.execute("DROP TABLE math_proficiency")
print("Table dropped... ")

#Commit your changes in the database
connection.commit()

#Closing the connection
connection.close()