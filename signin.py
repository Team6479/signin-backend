from flask import Flask, request, redirect, session
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "6749"

@app.route("/api")
def version():
    return "0.0.1"