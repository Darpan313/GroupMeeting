from flask import Flask,request 
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '34.68.237.67'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'Serverless_Users'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/register',methods=['POST'])
def Registration():
    post_data = request.get_json()
    name = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('pwd')
    topic = post_data.get('topic')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(name,email,password,topic) VALUES(%s,%s,%s,%s)",(name,email,password,topic))
    mysql.connection.commit()
    cur.close()
    response_object = {}
    response_object['message']='user inserted successfully!'
    return response_object, 200
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)