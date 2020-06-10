from flask import Flask,request 
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


@app.route('/register',methods=['POST'])
def Registration():
    post_data = request.get_json()
    name = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('pwd')
    topic = post_data.get('topic')
    cnx = pymysql.connect(**conf)
    cur = cnx.cursor()
    cur.execute("INSERT INTO users(name,email,password,topic) VALUES(%s,%s,%s,%s)",(name,email,password,topic))
    cnx.commit()
    cnx.close()
    response_object = {}
    response_object['message']='user inserted successfully!'
    return response_object, 200
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)