# math_only db
import csv
import sqlite3

# connect to database
connection = sqlite3.connect('math_student_proficiency.db')
# database cursor used to executive sql statements and fetch results
#   from sql queries
cursor = connection.cursor()

# creating a test table
create_table =  "CREATE TABLE match_proficiency("\
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "RCDTS INT," \
                "School Name TEXT," \
                "City TEXT," \
                "County TEXT," \
                "District Size TEXT," \
                "School Type TEXT," \
                "# Math Proficiency Total Student ," \
                "# Math Proficiency - Male," \
                "# Math Proficiency - Female," \
                "# Math Proficiency - White," \
                "# Math Proficiency - Black or African American," \
                "# Math Proficiency - Hispanic or Latino," \
                "# Math Proficiency - Asian," \
                "# Math Proficiency - Native Hawaiian or Other Pacific Islander," \
                "# Math Proficiency - American Indian or Alaska Native," \
                "# Math Proficiency - Two or More Races," \
                "# Math Proficiency - Children with Disabilities);"

# putting the math_proficiency table into our db
cursor.execute(create_table)

# open csv file we want to ingest into our db -> math_student_proficiency.db
file = open('math_only.csv')

# reading contents of csv
contents = csv.reader(file)

# sql query to insert data from csv into math_proficiency table
insert_records = "INSERT INTO math_proficiency " \
                 "(RCDTS," \
                 "School Name," \
                 "City," \
                 "County," \
                 "District Size," \
                 "School Type" \
                 "# Math Proficiency Total Student," \
                 "# Math Proficiency - Male," \
                 "# Math Proficiency - Female," \
                 "# Math Proficiency - White," \
                 "# Math Proficiency - Black or African American," \
                 "# Math Proficiency - Hispanic or Latino," \
                 "# Math Proficiency - Asian," \
                 "# Math Proficiency - Native Hawaiian or Other Pacific Islander," \
                 "# Math Proficiency - American Indian or Alaska Native," \
                 "# Math Proficiency - Two or More Races," \
                 "# Math Proficiency - Children with Disabilities) " \
                 "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

# importing contents of csv into math_only table
cursor.executemany(insert_records, contents)

# sql query retrieving all data from math_only table
#   to verify that the data from the cvs was successfully
#   inserted into the aforementioned table
select_all = "SELECT * FROM math_only"
rows = cursor.execute(select_all).fetchall()

# print to console
for r in rows():
    print(r)

# commit changes
connection.commit()

# close the db connection
connect.close()