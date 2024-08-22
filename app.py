from flask import Flask, request, jsonify
import os
from FormInfoExtractor import FormInfoExtractor  # Import your existing processing function

app = Flask(__name__)

@app.route('/')
def index():
    return 'Home Page!'

@app.route('/process')
def process():
    return 'Process Page!'

if __name__ == "__main__":
    app.run(debug=True)