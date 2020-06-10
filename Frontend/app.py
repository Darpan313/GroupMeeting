from flask import Flask, render_template,request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
#from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
import requests
import json
import datetime
from flask_cors import CORS
from datetime import timedelta
import pymysql

app = Flask(__name__) 
CORS(app)

'''app.config['MYSQL_HOST'] = '34.68.237.67'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'Serverless_Users'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' '''

conf = {
    "host": "34.68.237.67",
    "port": 3306,
    "user": "root",
    "passwd": "pass",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "database": "Serverless_Users"
}
app.permanent_session_lifetime = timedelta(minutes=5)

#mysql = MySQL(app)

TOPICS = [('Topic-1','Topic-1'),('Topic-2','Topic-2')]

loginurl = 'http://192.168.99.100:8083/login'
registrationurl = 'http://192.168.99.100:8082/register'
userstatusurl = 'http://192.168.99.100:8084/getUsers'

@app.route('/')
def index():
    return render_template('home.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    topic = SelectField('Topic', choices=TOPICS)
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        data = json.dumps({
            'username':username,
            'pwd':password_candidate
        })
        r = requests.post(loginurl,data=data, headers={"Content-Type":"application/json"})
        if r:
            data = json.loads(r.text)
            if(data['message']=='Username not found'):
                error = data['message']
                return render_template('login.html',error=error)
            elif(data['message']=='Invalid login'):
                error = data['message']
                return render_template('login.html',error=error)
            else:
                session['logged_in']=True
                session['username'] = username
                session['user_id'] = data['user_id']
                session['topic'] = data['topic']
                flash('You are now logged in!','success')
                return redirect(url_for('dashboard'))

    return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized. Please Login','danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/register', methods=['GET', 'POST'])
def Registration():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        topic = form.topic.data
        password = sha256_crypt.encrypt(str(form.password.data))
        data = json.dumps({
            'username':name,
            'email': email,
            'pwd': password,
            'topic': topic
        })
        #call api
        r = requests.post(registrationurl,data=data,headers={"Content-Type":"application/json"})
        if r:
            data = json.loads(r.text)
            print(data['message'])
            flash('You are now registered. Please log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/dashboard')
@is_logged_in
def dashboard():
    #get users and state
    #call api to get all users with same topic as current user and state
    data = json.dumps({
        'u_id':session['user_id']
    })
    r=requests.post(userstatusurl,data=data,headers={"Content-Type":"application/json"})
    if r:
        users = json.loads(r.text)
        print(users)
        return render_template('dashboard.html',users=users)
    
    return render_template('dashboard.html')

@app.route('/logout')
@is_logged_in
def logout():
    #cur = mysql.connection.cursor()
    cnx=pymysql.connect(**conf)
    cur = cnx.cursor()
    status = 'OFFLINE'
    cur.execute("UPDATE user_state SET status=%s,timestamp=%s WHERE id=%s",(status,datetime.datetime.now(),session['user_id']))
    cnx.commit()
    cnx.close()
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.secret_key = 'secret_123'
    app.run(host='0.0.0.0',port=5000,debug=True)