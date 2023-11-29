# Author : Rohan Lambe
# Date : 20/09/2023
# Description : This python script is responsible for creating a SQLite3 database
# file named "database.db" and creating a table in that database named as employee
# which will be used to store the data collected by the forms in this application
# we have to execute this script before testing or editing the main.py code.
# open python terminal and execute this script:
# python create_employee_table.py

import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

# Checks if the 'employee' table exists
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee'")
table_exists = cursor.fetchone()

if not table_exists:
    conn.execute('CREATE TABLE employee (name TEXT, addr TEXT, city TEXT,email TEXT)')
    print("Employee table has been created successfully.")
else:
    print("Employee table already exists.")

conn.close()
