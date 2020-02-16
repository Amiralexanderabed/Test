# Import MySQL Connector Driver
import mysql.connector as mysql

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = 'localhost' # different than inside the container and assumes default port of 3306

# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# # CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
cursor.execute("drop table if exists TStudents;")

# Create a TStudents table (wrapping it in a try-except is good practice)
try:
  cursor.execute("""
    CREATE TABLE TStudents (
      id integer  AUTO_INCREMENT PRIMARY KEY,
      first_name  VARCHAR(30) NOT NULL,
      last_name   VARCHAR(30) NOT NULL,
      email       VARCHAR(50) NOT NULL,
      pid         VARCHAR(20) NOT NULL,
      created_at  TIMESTAMP
    );
  """)
except:
  print("Table already exists. Not recreating it.")

# Insert Records
query = "insert into TStudents (first_name, last_name, email, pid, created_at) values (%s, %s, %s, %s, %s)"
values = [
  ('rick','gessner','rgessner@eng.ucsd.edu', 'A12345', '2020-02-11 12:00:00'),
  ('ramsin','khoshabeh','ramsin@eng.ucsd.edu', 'A23456', '2020-02-11 12:00:00'),
  ('steve','carrell','stevec@eng.ucsd.edu', 'A34567', '2020-02-11 12:00:00'),
  ('charleze','theron','charlezet@eng.ucsd.edu', 'A45678', '2020-02-11 12:00:00'),
  ('bryant','liu','briant@eng.ucsd.edu', 'A56789', '2020-02-11 12:00:00')
]
cursor.executemany(query, values)
db.commit()

# Selecting Records
cursor.execute("select * from TStudents;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]

db.close()