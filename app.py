from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import traceback

import pom_chob_khun_lift as pckl

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/')
def root():
    return "Working"

@app.route('/bof/')
def bof():
    page_list = [
        ['user list', '/bof/user_list'],
        ['user activity list', '/bof/user_activity_list'],
        ['raw lift state', '/liftstatus']
    ]
    return render_template('bof.html', page_list=page_list)


@app.route('/bof/user_list')
def bof_user_list():
    first = try_get(request.args.get('first'), 30)
    last = try_get(request.args.get('last'), 100)
    user_list = pckl.db.get_user_list(first, last)
    return render_template('user_list.html', user_list=user_list)

@app.route('/bof/user_activity_list')
def bof_user_activity_list():
    first = try_get(request.args.get('first'), 30)
    last = try_get(request.args.get('last'), 100)
    user_list = pckl.db.get_user_activity_list(first, last)
    return render_template('user_activity.html', user_list=user_list)

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
            #data = request.get_json()
            data = {}
            data['card_id'] = request.args.get('card_id')
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

@app.route('/liftcontrol', methods = ['POST', 'GET'])
def lift_control():
    try:
        if request.method == 'POST':
            data = request.get_json()
            return jsonify(pckl.post_lift_control(data))
        elif request.method == 'GET':
            data = {}
            data['lift_no'] = int(request.args.get('lift_no'))
            return jsonify(pckl.get_lift_control(data))
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"status": "server error"})

@app.route('/liftstatus', methods = ['POST', 'GET'])
def lift_status():
    try:
        if request.method == 'POST':
            data = request.get_json()
            return jsonify(pckl.lift_status(data))
        elif request.method == 'GET':
            return jsonify(pckl.get_lift_status())
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"status": "server error"})

@app.route('/liftcall', methods = ['GET'])
def lift_call():
    try:
        data = {}
        data['floor'] = int(request.args.get('floor'))
        data['going'] = request.args.get('going')
        return jsonify(pckl.lift_call(data))
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"status": "server error"})

def try_get(inp, default):
    return inp if inp != None else default

if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=5000)
