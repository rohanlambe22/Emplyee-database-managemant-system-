# Author: Rohan Lambe
# Date: 20/09/2023
# Description: This is Flask app that uses SQLite3 to
# execute Create ,Read ,Update, Delete operations

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


# Home page route
@app.route('/')
def home():
    return render_template('home.html')


# route to add new employee into the employee database
@app.route('/enternew')
def enternew():
    # It Instructs Flask to render an HTMl template
    return render_template('employee.html')


# route for add the new record (INSERT)  into the employee data to database
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():

    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            email = request.form['email']

            # connect to SQLite3 database and execute the INSERT
            with sqlite3.connect('C:\\Users\\Shourya\\Desktop\\flask_employee_management_project\\database.db') as con:
                # creating a cursor to execute the SQL queries
                cur = con.cursor()
                cur.execute("INSERT INTO employee (name,addr,city,email) VALUES(?, ?, ?, ?)", (nm, addr, city, email))

                # it is called to commit the transaction and save new record in database
                con.commit()
                msg = "Record successfully added"
        except Exception as e:
            # if exception occurs during insertion it rolls back transaction to maintain data consistency
            con.rollback()
            msg = f"error in insert operation: {str(e)}"

        finally:
            con.close()
            # sends the transaction message to result .html
            return render_template("result.html", msg=msg)


# it is the route for the SELECT all data from table and display it in table
@app.route('/list')
def list():
    con = sqlite3.connect('C:\\Users\\Shourya\\Desktop\\flask_employee_management_project\\database.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM employee")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


# used to update the database records
@app.route("/edit", methods=['POST', "GET"])
def edit():
    if request.method == 'POST':
        try:
            # it will retrieve the value of 'id' field from the form data
            id = request.form['id']

            con = sqlite3.connect('C:\\Users\\Shourya\\Desktop\\flask_employee_management_project\\database.db')
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM employee WHERE rowid = "+ id)

            # used to store the result of SELECT query which will contain
            # data of specific employee whose id matches the 'id' from the form.
            rows = cur.fetchall()
        except:
            id = None
        finally:
            con.close()

            return render_template("edit.html", rows=rows)

# it will update the data of an existing employee in SQLite database
# based on the changes made by the user in the edit form.
@app.route("/editrec", methods=['POST', 'GET'])
def editrec():
    if request.method == 'POST':
        try:
            rowid = request.form['rowid']
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            email = request.form['email']

            with sqlite3.connect('C:\\Users\\Shourya\\Desktop\\flask_employee_management_project\\database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE employee SET name='" + nm + "',addr='" + addr + "',city='" + city + "',email='" + email + "' WHERE rowid=" + rowid)

                con.commit()
                msg = "Record successfully edited in the database"

        except:
            con.rollback()
            msg = "Error in the Edit: UPDATE student SET name="+nm+",addr="+addr+", city="+city+",email="+email+" WHERE rowid="+rowid
        finally:
            con.close()

            return render_template('result.html', msg=msg)


# this route is used to delete the specific data from employee database
@app.route("/delete", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        try:
            rowid = request.form['id']
            with sqlite3.connect('C:\\Users\\Shourya\\Desktop\\flask_employee_management_project\\database.db') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM employee WHERE rowid=" + rowid)

                con.commit()
                msg = "Record Successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            return render_template('result.html', msg=msg)


if __name__ == '__main__':
    app.run(port=8010)

    # To run on port 801, uncomment the following line:
    #app.run(port=8011)
