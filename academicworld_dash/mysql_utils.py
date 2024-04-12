import mysql.connector

def connect_to_database():
    conn = mysql.connector.connect(user='root', password='your pass',
                                  host='localhost',
                                  database='academicworld')
    return conn

def execute_query(query, args=None):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(query,args)
    result = cursor.fetchall()
    conn.close()
    return result

def update_database(query, args=None):
    conn = connect_to_database()
    cursor = conn.cursor(prepared=True)
    if args:
        cursor.execute(query, args)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()

def get_last_three_keywords():
    cnx = connect_to_database()
    cursor = cnx.cursor()
    result_args = cursor.callproc('get_last_three_keywords')
    result = []
    for result_set in cursor.stored_results():
        for row in result_set.fetchall():
            result.append({'ID': row[0], 'Keyword': row[1]})
    cursor.close()
    cnx.close()
    return result


