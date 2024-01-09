# math_only db
import csv
import sqlite3

# connect to database (creating student.db)
connection = sqlite3.connect('student.db')
# database cursor used to executive sql statements and fetch results
#   from sql queries
cursor = connection.cursor()
'''
# creating a math_proficiency table (all school types)
#   should be school_name and school_type, no spaces on others
create_table =  "CREATE TABLE math_proficiency("\
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "RCDTS INTEGER," \
                "School_Name TEXT," \
                "City TEXT," \
                "County TEXT," \
                "District_Size TEXT," \
                "School_Type TEXT," \
                "No_Math_Proficiency_Total_Student INTEGER," \
                "No_Math_Proficiency_Male INTEGER," \
                "No_Math_Proficiency_Female INTEGER," \
                "No_Math_Proficiency_White INTEGER," \
                "No_Math_Proficiency_Black_or_African_American INTEGER," \
                "No_Math_Proficiency_Hispanic_or_Latino INTEGER," \
                "No_Math_Proficiency_Asian INTEGER," \
                "No_Math_Proficiency_Native_Hawaiian_or_Other_Pacific_Islander INTEGER," \
                "No_Math_Proficiency_American_Indian_or_Alaska_Native INTEGER," \
                "No_Math_Proficiency_Two_or_More_Races INTEGER," \
                "No_Math_Proficiency_Children_with_Disabilities INTEGER);"

# putting the math_proficiency table into our db
cursor.execute(create_table)

# open csv file we want to ingest into our db -> student.db
file = open('math_only.csv')

# reading contents of csv
contents = csv.reader(file)

# sql query to insert data from csv into math_proficiency table
insert_records = "INSERT INTO math_proficiency " \
                 "(RCDTS,"\
                 "School_Name," \
                 "City," \
                 "County," \
                 "District_Size," \
                 "School_Type," \
                 "No_Math_Proficiency_Total_Student," \
                 "No_Math_Proficiency_Male," \
                 "No_Math_Proficiency_Female," \
                 "No_Math_Proficiency_White," \
                 "No_Math_Proficiency_Black_or_African_American," \
                 "No_Math_Proficiency_Hispanic_or_Latino," \
                 "No_Math_Proficiency_Asian," \
                 "No_Math_Proficiency_Native_Hawaiian_or_Other_Pacific_Islander," \
                 "No_Math_Proficiency_American_Indian_or_Alaska_Native," \
                 "No_Math_Proficiency_Two_or_More_Races," \
                 "No_Math_Proficiency_Children_with_Disabilities) " \
                 "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

# importing contents of csv into math_proficiency table
cursor.executemany(insert_records, contents)

# sql query retrieving all data from math_proficiency table
#   to verify that the data from the cvs was successfully
#   inserted into the aforementioned table
select_all = "SELECT * FROM math_proficiency"
rows = cursor.execute(select_all).fetchall()

# print to console
for r in rows:
    print(r)

# commit changes
connection.commit()

# close the db connection
connection.close()
'''

# develop ela_proficiency table in student.db (all school types)
#   should be school_name and school_type, no spaces on others
create_table =  "CREATE TABLE ela_proficiency("\
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "RCDTS INTEGER," \
                "School_Name TEXT," \
                "City TEXT," \
                "County TEXT," \
                "District_Size TEXT," \
                "School_Type TEXT," \
                "No_ELA_Proficiency_Total_Student INTEGER," \
                "No_ELA_Proficiency_Male INTEGER," \
                "No_ELA_Proficiency_Female INTEGER," \
                "No_ELA_Proficiency_White INTEGER," \
                "No_ELA_Proficiency_Black_or_African_American INTEGER," \
                "No_ELA_Proficiency_Hispanic_or_Latino INTEGER," \
                "No_ELA_Proficiency_Asian INTEGER," \
                "No_ELA_Proficiency_Native_Hawaiian_or_Other_Pacific_Islander INTEGER," \
                "No_ELA_Proficiency_American_Indian_or_Alaska_Native INTEGER," \
                "No_ELA_Proficiency_Two_or_More_Races INTEGER," \
                "No_ELA_Proficiency_Children_with_Disabilities INTEGER);"

# putting the ela_proficiency table into our db
cursor.execute(create_table)

# open csv file we want to ingest into our db -> student.db
file = open('ela_only.csv')

# reading contents of csv
contents = csv.reader(file)

# sql query to insert data from csv into ela_proficiency table
insert_records = "INSERT INTO ela_proficiency " \
                 "(RCDTS,"\
                 "School_Name," \
                 "City," \
                 "County," \
                 "District_Size," \
                 "School_Type," \
                 "No_ELA_Proficiency_Total_Student," \
                 "No_ELA_Proficiency_Male," \
                 "No_ELA_Proficiency_Female," \
                 "No_ELA_Proficiency_White," \
                 "No_ELA_Proficiency_Black_or_African_American," \
                 "No_ELA_Proficiency_Hispanic_or_Latino," \
                 "No_ELA_Proficiency_Asian," \
                 "No_ELA_Proficiency_Native_Hawaiian_or_Other_Pacific_Islander," \
                 "No_ELA_Proficiency_American_Indian_or_Alaska_Native," \
                 "No_ELA_Proficiency_Two_or_More_Races," \
                 "No_ELA_Proficiency_Children_with_Disabilities) " \
                 "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

# importing contents of csv into ela_proficiency table
cursor.executemany(insert_records, contents)

# sql query retrieving all data from ela_proficiency table
#   to verify that the data from the cvs was successfully
#   inserted into the aforementioned table
select_all = "SELECT * FROM ela_proficiency"
rows = cursor.execute(select_all).fetchall()

# print to console
for r in rows:
    print(r)

# commit changes
connection.commit()

# close the db connection
connection.close()