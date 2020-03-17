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
        cursor = connection.cursor()
        # insert to user_data
        query_string = f"""
            INSERT INTO user_data (card_id, f_name, l_name, email, phone, created_on)
            VALUES ('{user_data['card_id']}',
                '{user_data['f_name']}',
                '{user_data['l_name']}',
                '{user_data['email']}',
                '{user_data['phone']}',
                CURRENT_TIMESTAMP
            )
            RETURNING user_id;
        """
        # print(query_string)
        cursor.execute(query_string)
        print(f"{cursor.rowcount} rows affected.")

        # insert to user_permission
        user_id = cursor.fetchone()[0]
        query_string = f"""
            INSERT INTO user_permission (user_id, available, created_on)
            VALUES ('{user_id}',
                '{user_data['permission']}',
                CURRENT_TIMESTAMP
            );
        """
        cursor.execute(query_string)
        connection.commit()
        print(f"{cursor.rowcount} rows affected.")
        cursor.close()
        return True
    return False

def check_permission_by_card(user_data):
    if(connection):
        cursor = connection.cursor()
        # select available floor from user_data & user_permission
        query_string = f"""
            SELECT user_permission.available FROM user_data, user_permission
            WHERE user_data.user_id = user_permission.user_id
            AND user_data.card_id = '{user_data['card_id']}';
        """
        # print(query_string)
        cursor.execute(query_string)
        if(cursor.rowcount):
            # card found
            available = cursor.fetchone()[0]
            print(available)
            available_floor = [int(floor) for floor in bin(available)[2:]]
        else:
            # card not found
            print('Card invalid !')
            available_floor = [0, 0, 0, 0]
        cursor.close()
        return available_floor
    return False
    
"""
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
"""
