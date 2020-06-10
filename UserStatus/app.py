from flask import Flask, request
import json
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

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

@app.route('/getUsers',methods=['POST'])
def getUsers():
    post_data = request.get_json()
    print(post_data)
    user_id = post_data.get('u_id')
    cnx = pymysql.connect(**conf)
    cur = cnx.cursor()
    cur.execute('SELECT p.id,name,status,topic FROM (SELECT * FROM user_state) as p,(SELECT * FROM users WHERE topic = (select topic from users where id=%s)) as t WHERE p.id = t.id AND p.id != %s;',(user_id,user_id))
    users = cur.fetchall()
    cnx.close()
    return json.dumps(users),200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5003,debug=True)