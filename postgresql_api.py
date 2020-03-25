import psycopg2
import os
try:
    """
    connection = psycopg2.connect(user = os.environ["PG_USER"],
                                  password = os.environ["PG_PASSWORD"],
                                  host = os.environ["PG_HOST"],
                                  port = os.environ["PG_PORT"],
                                  database = os.environ["PG_DATABASE"])
    """
    connection = psycopg2.connect(os.environ["DATABASE_URL"])
    connection.set_session(autocommit=True)
    cur = connection.cursor()
    cur.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public'
    AND table_type='BASE TABLE';
    """)
    rows = cur.fetchall()
    print('Table list:')
    for row in rows:
        print("   ", row[0])
    cur.close()

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)

def add_user(user_data):
    if(connection):
        status = None
        cursor = connection.cursor()
        # insert to user_data
        query_string = f"""
            INSERT INTO user_data (card_id, f_name, l_name, email, phone, created_on)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING user_id;
        """
        # print(query_string)
        cursor.execute(query_string, (
            user_data['card_id'],
            user_data['f_name'],
            user_data['l_name'],
            user_data['email'],
            user_data['phone']
        ))
        print(f"{cursor.rowcount} rows affected.")

        # insert to user_permission
        user_id = cursor.fetchone()[0]
        query_string = f"""
            INSERT INTO user_permission (user_id, available, created_on)
            VALUES (%s, %s, NOW());
        """
        cursor.execute(query_string, (user_id, user_data['permission']))
        print(f"{cursor.rowcount} rows affected.")
        cursor.close()
        return (True, status)
    return (False, status)

def check_permission_by_card(user_data):
    if(connection):
        status = None
        cursor = connection.cursor()
        # select available floor from user_data & user_permission
        query_string = f"""
            SELECT user_data.user_id, user_permission.available FROM user_data, user_permission
            WHERE user_data.user_id = user_permission.user_id
            AND user_data.card_id = %s
            AND NOT user_data.is_deleted;
        """
        # print(query_string)
        cursor.execute(query_string, (user_data['card_id'], ))
        event_id = -1
        if(cursor.rowcount):
            # card found
            user_id, available = cursor.fetchone()
            #print(available)
            available_floor = [int(floor) for floor in bin(available)[2:]]

            # update activity&active date
            query_string = f"""
                UPDATE user_data
                SET last_active = NOW(), status = 'CHECKED IN'
                WHERE user_id = %s;

                INSERT INTO user_activity (user_id, lift_no, created_on, arrival)
                VALUES (%s, %s, NOW(), %s)
                RETURNING id;
            """
            cursor.execute(query_string, (user_id, user_id, user_data['lift_no'], user_data['arrival']))
            event_id = cursor.fetchone()[0]
            print(f"{cursor.rowcount} rows affected.")
        else:
            # card not found
            print('Card invalid !')
            available_floor = [0, 0, 0, 0]
            status = "Card not found"
        cursor.close()
        return (available_floor, event_id, status)
    return False

def check_permission_by_id(user_data):
    if(connection):
        status = None
        cursor = connection.cursor()
        # select available floor from user_data & user_permission
        query_string = f"""
            SELECT user_permission.available FROM user_data, user_permission
            WHERE user_data.user_id = user_permission.user_id
            AND user_data.user_id = %s
            AND NOT user_data.is_deleted;
        """
        # print(query_string)
        cursor.execute(query_string, (user_data['user_id'], ))
        if(cursor.rowcount):
            # User found
            query_result = cursor.fetchone()
            available = query_result[0]
            #print(available)
            available_floor = [int(floor) for floor in bin(available)[2:]]
        else:
            # User not found
            print('User not found !')
            available_floor = [0, 0, 0, 0]
            status = "User not found"
        cursor.close()
        return (available_floor, status)
    return False
    
def find_user_id(user_data):
    if(connection):
        status = None
        cursor = connection.cursor()
        query_string = f"""
            SELECT user_id FROM user_data
            WHERE card_id = %s
            AND NOT user_data.is_deleted;
        """
        cursor.execute(query_string, (user_data['card_id'], ))
        if(cursor.rowcount):
            # Card found
            query_result = cursor.fetchone()
            user_id = query_result[0]
        else:
            # Card not found
            user_id = -1
            status = "Card not found"
        cursor.close()
        return (user_id, status)
    return False

def update_user_activity(event_id, target):
    if(connection):
        cursor = connection.cursor()
        query_string = f"""
            UPDATE user_activity
            SET departure = %s
            WHERE id = %s
            RETURNING user_id;
        """
        cursor.execute(query_string, (target, event_id, ))
        if(not cursor.rowcount):
            return "event not found"
        user_id = cursor.fetchone()[0] 
        query_string = f"""
            UPDATE user_data
            SET last_active = NOW(), last_stop = %s, status = NULL
            WHERE user_id = %s;
        """
        cursor.execute(query_string, (target, user_id, ))
        cursor.close()
        return None
    return 'database error'

def remove_user(user_data):
    if(connection):
        status = None
        cursor = connection.cursor()
        query_string = f"""
            UPDATE user_data
            SET is_deleted = True
            WHERE user_id = %s;
        """
        cursor.execute(query_string, (user_data['user_id'], ))
        cursor.close()
        if(not cursor.rowcount):
            status = "card not found"
        return status
    return 'database error'
    
def update_lift_activity(lift_no, floor, event_no):
    if(connection):
        cursor = connection.cursor()
        query_string = f"""
            INSERT INTO lift_activity (lift_no, created_on, floor, event_no)
            VALUES (%s, NOW(), %s, %s);
        """
        cursor.execute(query_string, (lift_no, floor, event_no, ))
        cursor.close()
        return None
    return 'database error'

"""
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
"""
