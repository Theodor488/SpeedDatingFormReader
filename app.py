from flask import Flask, request, jsonify, render_template, url_for
import os
from FormInfoExtractor import FormInfoExtractor  # Import your existing processing function

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process')
def process():
    return 'Process Page!'

if __name__ == "__main__":
    app.run(debug=True)