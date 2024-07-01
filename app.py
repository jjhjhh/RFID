from flask import Flask, request, jsonify, render_template
import json
from datetime import datetime
import pytz #korea time

app = Flask(__name__)

#time setting
kr_tz = pytz.timezone('Asia/Seoul')

# Load users.json
with open('users.json') as f:
    valid_uids = {user['uid']: user for user in json.load(f)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_users', methods=['GET'])
def get_users():
    return jsonify(list(valid_uids.values()))

@app.route('/update_uid', methods=['POST']) #POST
def update_uid():
    data = request.get_json()
    uid = data.get('uid')
    
    user = valid_uids.get(uid)
    
    if user:
        current_time = datetime.now(kr_tz).strftime('%H:%M')

        if user['checked_in']: #already exists, record end_time
            user['end_time'] = current_time
            user['checked_in'] = False #end_time === False
            message = str(uid)+' end_time update! '+current_time
            print(str(uid)+' end_time update! '+current_time)
        else:
            user['start_time'] = current_time
            user['checked_in'] = True
            message = str(uid)+' start_time update! '+current_time
            print(str(uid)+' start_time update! '+current_time)

        return jsonify({'status': 'success', 'uid': uid, 'username': user['username'], 'time': current_time, 'message': message})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid UID'}), 400

if __name__ == '__main__':
    app.run(debug=True)
