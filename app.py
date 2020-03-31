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

################## BOF Zone ##################

@app.route('/bof/')
def bof():
    page_list = [
        ['User List', '/bof/user_list'],
        ['User Activity', '/bof/user_activity_list'],
        ['User Detail (ex. 39)', '/bof/user/39'],
        ['Lift Activity', '/bof/lift_activity_list'],
        ['Lift Status', '/bof/lift_status'],
        ['OLED emulator', '/bof/oled_terminal']
    ]
    return render_template('bof.html', page_list=page_list)

@app.route('/bof/lift_activity_list')
def bof_lift_activity_list():
    try:
        first = try_get(request.args.get('first'), 30)
        last = try_get(request.args.get('last'), 100)
        lift_activity_list = pckl.db.lift_activity_list(first, last)
        return render_template('lift_activity_list.html', lift_activity_list=lift_activity_list)
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return render_template('5xx.html')

@app.route('/bof/user/<user_id>')
def bof_user(user_id):
    try:
        data = pckl.db.get_user_data(user_id)
        user_activity = pckl.db.get_user_activity(user_id)
        print(user_activity)
        return render_template('user_data.html', data=data, user_activity=user_activity)
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return render_template('5xx.html')

@app.route('/bof/lift_status')
def bof_lift_status():
    try:
        lift = pckl.get_lift_status()
        lift_activity_1 = pckl.db.lift_activity_detail(1)
        lift_activity_2 = pckl.db.lift_activity_detail(2)
        return render_template('lift_status.html', 
            lift=lift,
            lift_activity_1=lift_activity_1,
            lift_activity_2=lift_activity_2)
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return render_template('5xx.html')

@app.route('/bof/oled_terminal')
def bof_oled_terminal():
    try:
        data = pckl.scan.lift
        return render_template('oled_terminal.html', data=data)
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return render_template('5xx.html')

@app.route('/bof/user_list')
def bof_user_list():
    try:
        first = try_get(request.args.get('first'), 30)
        last = try_get(request.args.get('last'), 100)
        user_list = pckl.db.get_user_list(first, last)
        return render_template('user_list.html', user_list=user_list)
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return render_template('5xx.html')

@app.route('/bof/user_activity_list')
def bof_user_activity_list():
    try:
        show = try_get(request.args.get('show'), 30)
        user_list = pckl.db.get_user_activity_list(show)
        return render_template('user_activity.html', user_list=user_list)
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return render_template('5xx.html')

################## APIs Zone ##################

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

@app.route('/liftcall', methods = ['POST'])
def lift_call():
    try:
        data = request.get_json()
        return jsonify(pckl.lift_call(data))
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"status": "server error"})

def try_get(inp, default):
    return inp if inp != None else default

if __name__ == "__main__":
    app.run(debug = False, host="0.0.0.0", port=5000)
