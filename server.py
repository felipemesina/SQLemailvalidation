from flask import Flask, render_template, redirect, request, session, flash
from datetime import datetime
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
mysql = MySQLConnector(app, 'emailvalidation')
app.secret_key = "rooter"

@app.route('/')
def index():
    return render_template('index.html')


def create(request):
    query = "INSERT INTO email (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
    data = {
            'email': request.form['email']
            }
    mysql.query_db(query, data)

def display():
    query = "SELECT * FROM email"
    emails = mysql.query_db(query)
    return render_template('process.html', emails=emails)

@app.route('/signup', methods=['POST'])
def result():
    check = True
    if len(request.form['email']) < 1:
        flash('Error! Invalid email', 'wrong')
        check = False
        return render_template('process.html')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid email format. Please try again.', 'wrong')
        check = False
        return render_template('process.html')
    if check == True:
        flash('The email address you entered is a valid email address. Thank you!', 'success')
        create(request)
        return display()






app.run(debug = True)
