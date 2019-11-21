from flask import Flask, request, redirect, session, abort
import json
import os
import json
import dummy_aws as aws

app = Flask(__name__)

try:
    os.makedirs('data/users')
except:
    print('Data directory already exists, skipping')

# I acknowledge the downsides of this line
app.secret_key = os.urandom(16)

@app.route('/')
def home():
    return '6749'

@app.route('/api', methods=['GET', 'POST'])
def version():
    return '0.0.1'

@app.route('/api/get/user', methods=['POST'])
def get_user_data():
    id = int(request.form['id'])
    data = aws.get_user_data(id)
    if data:
        return json.dumps(data)
    else:
        abort(404)

@app.route('/api/put/user', methods=['POST'])
def make_user():
    id = int(request.form['id'])
    if aws.get_user_data(id):
        abort(409)
    else:
        aws.create_user(id, request.form['name'])

@app.route('/api/put/entry', methods=['POST'])
def push_entry():
    id = int(request.form['id'])
    start = int(request.form['start'])
    end = int(request.form['end'])
    aws.push_entry(id, start, end)