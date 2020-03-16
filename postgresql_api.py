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
        query_string = f"""
            INSERT INTO user_data (card_id, f_name, l_name, email, phone, created_on)
            VALUES ('{user_data['card_id']}',
                '{user_data['f_name']}',
                '{user_data['l_name']}',
                '{user_data['email']}',
                '{user_data['phone']}',
                CURRENT_TIMESTAMP
            );
        """
        print(query_string)
        cursor = connection.cursor()
        cursor.execute(query_string)
        connection.commit()
        cursor.close()
        #print(data)
        return f"{cursor.rowcount} rows affected."
    return False

"""
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
"""
