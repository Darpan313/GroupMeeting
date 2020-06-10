from flask import Flask, request
from flask_mysqldb import MySQL
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = '34.68.237.67'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'Serverless_Users'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/getUsers',methods=['POST'])
def getUsers():
    post_data = request.get_json()
    print(post_data)
    user_id = post_data.get('u_id')
    cur = mysql.connection.cursor()
    cur.execute('SELECT p.id,name,status,topic FROM (SELECT * FROM user_state) as p,(SELECT * FROM users WHERE topic = (select topic from users where id=%s)) as t WHERE p.id = t.id AND p.id != %s;',(user_id,user_id))
    users = cur.fetchall()
    cur.close()
    return json.dumps(users),200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5003,debug=True)