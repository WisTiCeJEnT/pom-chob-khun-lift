from flask import Flask, request, jsonify
from flask_cors import CORS

import sys
import json
import traceback

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/')
def root():
    return "Working"

@app.route('/adduser', methods = ['POST'])
def add_user():
    try:
        if request.method == 'POST':
            data = request.get_json()
            return jsonify({"status": "ok",
                            "uid": data["uid"]})
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"status": "error"})

if __name__ == "__main__":
    app.run(debug = False,host="0.0.0.0", port=5000)
