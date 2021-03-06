from flask import Flask, request
from passlib.hash import sha256_crypt
import datetime
import pymysql

app = Flask(__name__)

'''app.config['MYSQL_HOST'] = '34.68.237.67'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'Serverless_Users'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)'''

conf = {
    "host": "34.68.237.67",
    "port": 3306,
    "user": "root",
    "passwd": "pass",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "database": "Serverless_Users"
}

@app.route('/login',methods=['POST'])
def login():
    response_object = {}
    post_data = request.get_json()
    username = post_data.get('username')
    password = post_data.get('pwd')

    #cur = mysql.connection.cursor()
    cnx = pymysql.connect(**conf)
    cur = cnx.cursor()
    result = cur.execute("SELECT * FROM users WHERE name = %s",[username])
    if result > 0:
        data = cur.fetchone()
        pwd = data['password']
        u_id = data['id']
        topic = data['topic']
        print(password)
        if sha256_crypt.verify(password,pwd):
            response_object['message']='user logged in successfully!'
            response_object['user_id'] = u_id
            response_object['topic'] = topic
            status = 'ONLINE'
            cur.execute("REPLACE INTO user_state (id,status,timestamp) VALUES(%s,%s,%s)",(u_id,status,datetime.datetime.now()))
            cnx.commit()
        else:
            error = 'Invalid login'
            response_object['message'] = error
        cnx.close()
    else:
        error = 'Username not found'
        response_object['message'] = 'Username not found'
    return response_object, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002,debug=True)