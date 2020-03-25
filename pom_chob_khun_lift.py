import postgresql_api as db

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