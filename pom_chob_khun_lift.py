import postgresql_api as db
import scan

def add_user(raw_data):
    user_data = raw_data
    user_data['permission'] = int(f'0b'+''.join([str(c) for c in raw_data['permission']]), 2)
    db_result, status = db.add_user(user_data)
    if(db_result):
        return {
            'status': status if status != None else "ok",
        }
    else:
        return {
            'status': 'database error',
        }

def check_permission(raw_data):
    if raw_data['card_id']:
        available_floor, event_id, status = db.check_permission_by_card(raw_data)
        if(available_floor):
            return {
                'status': status if status != None else "ok",
                'available_floor': available_floor,
                'event_id': event_id
            }
        else:
            return {
                'status': 'database error',
            }
    elif raw_data['card_id']:
        available_floor, status = db.check_permission_by_id(raw_data)
        if(available_floor):
            return {
                'status': status if status != None else "ok",
                'available_floor': available_floor
            }
        else:
            return {
                'status': 'database error',
            }

def find_user_id(raw_data):
    user_id, status = db.find_user_id(raw_data)
    if(user_id):
        return {
            'status': status if status != None else "ok",
            'user_id': user_id
            }
    else:
        return {
            'status': 'database error',
        }
        
def remove_user(raw_data):
    status = db.remove_user(raw_data)
    return {
        'status': status if status != None else "ok",
    }

def update_user_activity(raw_data):
    status = db.update_user_activity(
        event_id = raw_data['event_id'], 
        target = raw_data['target']
        )
    scan.add_queue(
        lift_no = raw_data['lift_no'],
        dest = raw_data['target']
        )
    return {
        'status': status if status != None else "ok",
    }

def update_lift_activity(raw_data):
    status = db.update_lift_activity(
        lift_no = raw_data['lift_no'], 
        floor = raw_data['floor'], 
        event_no = raw_data['event']
        )
    return {
        'status': status if status != None else "ok",
    }

def get_lift_control(raw_data):
    lift_no = raw_data['lift_no']
    door_open = None
    status = None
    oled = None
    if scan.lift[lift_no]['status'] == 'OPEN':
        door_open = 1
        oled = 'OPEN'
        scan.lift[lift_no]['status'] = 'WAITING'
    else:
        door_open = 0
        oled = str(scan.lift[lift_no]['floor'])
    return {
        'door_open': door_open,
        'oled': oled,
        'status': status if status != None else "ok",
    }

def post_lift_control(raw_data):
    lift_no = raw_data['lift_no']
    status = None
    if scan.lift[lift_no]['status'] == 'WAITING':
        scan.lift[lift_no]['status'] = 'CLOSE'
    return {
        'status': status if status != None else "ok",
    }

def lift_status(raw_data):
    status = None
    lift_2_position = None
    lift_1_position = None
    if 'lift_1_position' in raw_data:
        lift_1_position = raw_data['lift_1_position']
    if 'lift_2_position' in raw_data:
        lift_2_position = raw_data['lift_2_position']
    lift_1_move = scan.update_lift_status(lift_no=1, floor=lift_1_position)
    lift_2_move = scan.update_lift_status(lift_no=2, floor=lift_2_position)
    return {
        'lift_1_move': lift_1_move,
        'lift_2_move': lift_2_move,
        'status': status if status != None else "ok",
    }

def get_lift_status():
    status = None
    return {
        'lift_1': scan.lift[1],
        'lift_2': scan.lift[2],
        'status': status if status != None else "ok",
    }

def lift_call(raw_data):
    status = None
    scan.new_user(
        floor=raw_data['floor'],
        going=raw_data['going']
    )
    return {
        'status': status if status != None else "ok",
    }