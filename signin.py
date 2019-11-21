from flask import Flask, request, redirect, session, abort
import json
import os
import dynamo_json as json
import aws

app = Flask(__name__)

# I acknowledge the downsides of this line
app.secret_key = os.urandom(16)

API_KEYS = os.environ['API_KEYS'].split(':')

@app.route('/')
def home():
    return '6749'

@app.route('/api', methods=['GET', 'POST'])
def version():
    return '0.0.1'

@app.route('/api/get/user', methods=['POST'])
def get_user_data():
    if not request.form['key'] in API_KEYS:
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
        abort(401)
    id = int(request.form['id'])
    start = int(request.form['start'])
    end = int(request.form['end'])
    aws.push_entry(id, start, end)
    return str(id)