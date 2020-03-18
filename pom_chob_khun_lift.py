import postgresql_api as db

def add_user(raw_data):
    user_data = raw_data
    user_data['permission'] = int(f'0b'+''.join([str(c) for c in raw_data['permission']]), 2)
    if(db.add_user(user_data)):
        return {
            'status': 'ok',
        }
    else:
        return {
            'status': 'database error',
        }

def check_permission(raw_data):
    if 'card_id' in raw_data:
        available_floor, event_id = db.check_permission_by_card(raw_data)
        if(available_floor):
            return {
                'status': 'ok',
                'available_floor': available_floor,
                'event_id': event_id
            }
        else:
            return {
                'status': 'database error',
            }
    elif 'user_id' in raw_data:
        available_floor = db.check_permission_by_id(raw_data)
        if(available_floor):
            return {
                'status': 'ok',
                'available_floor': available_floor
            }
        else:
            return {
                'status': 'database error',
            }
    