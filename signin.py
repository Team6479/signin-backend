from flask import Flask, request, redirect, session, abort, render_template
import json
import os
import dynamo_json as json
import aws
import util

app = Flask(__name__)

# I acknowledge the downsides of this line
app.secret_key = os.urandom(16)

API_KEYS = os.environ['API_KEYS'].split(':')

@app.route('/')
def home():
    return redirect('/login', code=301)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    if not request.form['key'] in API_KEYS:
        print('Invalid API key: ' + request.form['key'])
        abort(401)
    id = int(request.form['id'])
    data = aws.get_user_data(id)
    if data:
        entries = aws.get_entries(id)
        table_data = []
        secs = 0
        for entry in entries:
            secs += entry['end'] - entry['start']
            table_data.append([util.fdate_from_dt(entry['start']), util.fsec(entry['end'] - entry['start']), util.ftime_from_dt(entry['start']), util.ftime_from_dt(entry['end'])])
        leaderboard = []
        for user in aws.get_all_users_long():
            leaderboard.append([user['name'], user['id'], util.fsec(user['time'])])
        leaderboard.sort(key=(lambda user: user[2]), reverse=True)
        return render_template("user.html", id=id, name=data['name'], table_data=table_data, leaderboard=leaderboard[:10], time=util.fsec(secs), secs=secs)
    else:
        abort(404)

@app.route('/api', methods=['GET', 'POST'])
def version():
    return '0.2'

@app.route('/api/ping', methods=['GET', 'POST'])
def ping():
    return 'ping'

@app.route('/api/key/check', methods=['POST'])
def check_key():
    if not request.form['key'] in API_KEYS:
        return 'false', 401
    else:
        return 'true'

@app.route('/api/get/user', methods=['POST'])
def get_user_data():
    if not request.form['key'] in API_KEYS:
        print('Invalid API key: ' + request.form['key'])
        abort(401)
    id = int(request.form['id'])
    data = aws.get_user_data(id)
    if data:
        return json.dumps(data)
    else:
        abort(404)

@app.route('/api/put/user', methods=['POST'])
def make_user():
    if not request.form['key'] in API_KEYS:
        print('Invalid API key: ' + request.form['key'])
        abort(401)
    id = int(request.form['id'])
    if aws.get_user_data(id):
        abort(409)
    else:
        aws.create_user(id, request.form['name'])
        return str(id)

@app.route('/api/put/entry', methods=['POST'])
def push_entry():
    if not request.form['key'] in API_KEYS:
        print('Invalid API key: ' + request.form['key'])
        abort(401)
    id = int(request.form['id'])
    start = int(request.form['start'])
    end = int(request.form['end'])
    aws.push_entry(id, start, end)
    return str(id)

@app.route('/api/get/entries', methods=['POST'])
def get_entries():
    if not request.form['key'] in API_KEYS:
        print('Invalid API key: ' + request.form['key'])
        abort(401)
    id = int(request.form['id'])
    return json.dumps(aws.get_entries(id))