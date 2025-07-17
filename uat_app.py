from Demos.win32ts_logoff_disconnected import username
from flask import Flask, render_template, request, url_for, session, redirect
from jira import JIRA
import mysql.connector
from datetime import *
import time as t
import re

app = Flask(__name__)
app.secret_key = 'abdeali@123'

@app.route("/")
def index():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'] )
    return redirect(url_for('login_page'))

@app.route("/index")
def home():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'] )
    return redirect(url_for('login_page'))

@app.route("/trainer")
def trainer():
    if 'loggedin' in session:
        return render_template('trainer_form.html', username=session['username'] )
    return redirect(url_for('login_page'))

@app.route("/trainer_create",methods=['POST','GET'])
def trainer_create():

    if request.method == 'POST':
        fname_data = request.form['fname']
        lname_data = request.form['lname']
        desig_data = request.form['desig']
        course_data = request.form['course']

        sql = "INSERT INTO trainer_details (fname,lname,desig,course) VALUES (%s,%s,%s,%s)"
        val = (fname_data,lname_data,desig_data,course_data)

        conn = mysql.connector.connect(
            host="192.168.1.26",
            user="mysql_user",
            password="alnafi",
            database="alnafi"
        )
        cursor = conn.cursor()
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()


        return render_template('trainer_form.html')

@app.route("/trainer_data",methods=['POST','GET'])
def trainer_data():
    if 'loggedin' not in session:
        return redirect(url_for('login_page'))
    conn = mysql.connector.connect(
        host="192.168.1.26",
        user="mysql_user",
        password="alnafi",
        database="alnafi"
    )
    cursor = conn.cursor()
    sql = "select * from trainer_details"
    cursor.execute(sql)
    row = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('trainer_report.html', output_data=row, username=session['username'])

@app.route("/trainer_filter", methods=['POST', 'GET'])
def trainer_filter():

    if request.method == 'POST':
        course_search = request.form['course']

        conn = mysql.connector.connect(
            host="192.168.1.26",
            user="mysql_user",
            password="alnafi",
            database="alnafi"
        )
        cursor = conn.cursor()


    sql = "SELECT * FROM trainer_details WHERE course = %s"
    cursor.execute(sql, (course_search,))

    row = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('trainer_report.html', output_data=row)

@app.route("/jira")
def jira():
    if 'loggedin' in session:
        return render_template('jira_page.html', username=session['username'] )
    return redirect(url_for('login_page'))

@app.route("/jira_create", methods = ['POST','GET'])
def jira_create():
    if request.method == "POST":
        project_data = request.form['project']
        issuetype_data = request.form['issuetype']
        reporter_data = request.form['reporter']
        summary_data = request.form['summary']
        desc_data = request.form['desc']
        priority_data = request.form['priority']
        server = "https://naveedzafar.atlassian.net"
        user = "zafarn@evergegroup.com"
        apitoken = ""
        jira= JIRA(server,basic_auth=(user,apitoken))
        issue = jira.create_issue(project=project_data,summary=summary_data,issuetype=issuetype_data,description=desc_data,priority={'name':priority_data})
        print(issue)
        return render_template("jira_page.html")

@app.route("/login_page")
def login_page():
    return render_template("login.html")


@app.route("/",methods = ['POST','GET'])
def login():
    msg=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connector.connect(
            host="192.168.1.26",
            user="mysql_user",
            password="alnafi",
            database="alnafi"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute( "select * from users where username = %s and password = %s" , (username , password))
        account = cursor.fetchone()
        print(account)
        if account:
            session['loggedin']=True
            session['id'] = account ['id']
            session['username'] = account['username']
            return render_template("index.html",username=session['username'])
        else:
            msg = "Incorrect Username/Passowrd!!!"
    return render_template("login.html", msg=msg)

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/create_account",methods = ['POST','GET'])
def create_account():
    msg=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn = mysql.connector.connect(
            host="192.168.1.26",
            user="mysql_user",
            password="alnafi",
            database="alnafi"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute( "select * from users where username = %s " , (username,))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = "Username already exist!!!!"
            return render_template('register.html' , msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid Email Format"
            return render_template('register.html', msg=msg)
        else:
            cursor.execute('INSERT INTO users values (NULL, %s,%s,%s)',(username,password,email,))
            conn.commit()
            msg = "Successfully registered!!!"
    elif request.method == "POST":
        msg = "Please enter the details !!!!"
    return render_template('register.html', msg = msg)


@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login_page'))




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")