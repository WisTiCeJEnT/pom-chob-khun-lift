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
            'status': 'error',
        }