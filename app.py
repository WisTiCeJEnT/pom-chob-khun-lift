from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

import pom_chob_khun_lift as pckl

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
            return jsonify(pckl.add_user(data))
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"status": "server error"})

@app.route('/checkpermission', methods = ['GET'])
def check_permission():
    try:
        if request.method == 'GET':
            #data = request.get_json()
            data = {}
            data['card_id'] = request.args.get('card_id')
            data['user_id'] = request.args.get('user_id')
            data['arrival'] = request.args.get('arrival')
            data['lift_no'] = request.args.get('lift_no')
            return jsonify(pckl.check_permission(data))
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"status": "server error"})

@app.route('/finduserid', methods = ['GET'])
def find_user_id():
    try:
        if request.method == 'GET':
            data = request.get_json()
            return jsonify(pckl.find_user_id(data))
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"status": "server error"})

@app.route('/removeuser', methods = ['DELETE'])
def remove_user():
    try:
        if request.method == 'DELETE':
            data = request.get_json()
            return jsonify(pckl.remove_user(data))
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"status": "server error"})

@app.route('/useractivity', methods = ['PATCH'])
def update_user_activity():
    try:
        if request.method == 'PATCH':
            data = request.get_json()
            return jsonify(pckl.update_user_activity(data))
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"status": "server error"})

@app.route('/liftactivity', methods = ['POST', 'GET'])
def lift_activity():
    try:
        if request.method == 'POST':
            data = request.get_json()
            return jsonify(pckl.update_lift_activity(data))
        elif request.method == 'GET':
            data = request.get_json()
            return jsonify({"status": "comming soon"})
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"status": "server error"})

if __name__ == "__main__":
    app.run(debug = False,host="0.0.0.0", port=5000)
