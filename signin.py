from flask import Flask, request, redirect, session
import json
import os

app = Flask(__name__)

# I acknowledge the downsides of this line
app.secret_key = os.urandom(16)

@app.route("/")
def home():
    return "6749"

@app.route("/api")
def version():
    return "0.0.1"