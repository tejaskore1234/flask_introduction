# routes.py

import sqlite3 as sql

from main import app
from flask import render_template, request

# connect to qa_database.sq (database will be created, if not exist)
con = sql.connect('PersonalDetail.db')
con.execute('CREATE TABLE IF NOT EXISTS Personal (Id INTEGER PRIMARY KEY AUTOINCREMENT,'
            + 'Website TEXT, Username TEXT, Password TEXT, EmailId TEXT)')
con.close

# home page
@app.route('/')  # root : main page
def index():
    # by default, 'render_template' looks inside the folder 'template'
    return render_template('index.html')

# Create question
@app.route('/enter', methods=['GET', 'POST'])
def enter():
    if request.method == 'GET':
        # send the form
        return render_template('enter.html')
    else: # request.method == 'POST':
        # read data from the form and save in variable
        Website = request.form['website']
        Username = request.form['username']
        Password = request.form['password']
        EmailId = request.form['emailid']

        # store in database
        try:
            con = sql.connect('PersonalDetail.db')
            c =  con.cursor() # cursor
            # insert data
            c.execute("INSERT INTO Personal (Website, Username, Password, EmailId) VALUES (?,?,?,?)",
                (Website, Username, Password, EmailId))
            con.commit() # apply changes
            # go to thanks page
            return render_template('enteredThanks.html')
        except con.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('database_error.html', error=err)
        finally:
            con.close() # close the connection


# Display question
@app.route('/view')
def view():
        try:
            con = sql.connect('PersonalDetail.db')
            c =  con.cursor() # cursor
            # read question : SQLite index start from 1 (see index.html)
            query = "Select * FROM Personal"
            c.execute(query)
            record_list = c.fetchall() # fetch the data from cursor
            #con.commit() # apply changes
            # go to thanks page : pass the value of tuple using question[0]
            return render_template('view.html', rec_list=record_list)
        except con.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('database_error.html', error=err)
        finally:
            con.close() # close the connection

#        return render_template('question.html', question=question)

@app.route('/delete_all')
def delete_all():
        try:
            con = sql.connect('PersonalDetail.db')
            c =  con.cursor() # cursor
            # read question : SQLite index start from 1 (see index.html)
            query = "DELETE FROM Personal"
            c.execute(query)
            con.commit() # apply changes
            # go to thanks page : pass the value of tuple using question[0]
            return render_template('deleteThanks.html')
        except con.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('database_error.html', error=err)
        finally:
            con.close() # close the connection

#        return render_template('question.html', question=question)
