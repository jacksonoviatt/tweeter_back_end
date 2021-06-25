from flask.wrappers import Response
import mariadb
import dbconnect
import traceback


# The same comments apply to all the helper functions in here!
def run_select_statement(sql, params):
    # Do the normal open and variable setup
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    # Try to run the command based on the SQL and params passed in
    try:
        cursor.execute(sql, params)
        result = cursor.fetchall()
    # TODO Do a better job of catching more specific errors! Might need to find a way to return error-specific results
    except:
        traceback.print_exc()
        print("DO BETTER ERROR CATCHING")

    # Close the resources
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # Return the result
    return result


def run_insert_statement(sql, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    try:
        cursor.execute(sql, params)
        conn.commit()
        result = cursor.lastrowid
    except:
        traceback.print_exc()
        print("DO BETTER ERROR CATCHING")

    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    return result


def run_delete_statement(sql, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    try:
        cursor.execute(sql, params)
        conn.commit()
        result = cursor.rowcount
    except:
        traceback.print_exc()
        print("DO BETTER ERROR CATCHING")

    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    return result


def run_update_statement(sql, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    try:
        cursor.execute(sql, params)
        conn.commit()
        result = cursor.rowcount
    except:
        traceback.print_exc()
        print("DO BETTER ERROR CATCHING")

    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    return result

def update_specific_column(table, column, new_data, user_id, key):
    # this is specific to the users table,
    sql = run_update_statement(f"UPDATE {table} SET {column}=? WHERE {key}=?", [new_data, user_id])
    return sql    

def get_user_info(column, token):
    user_info = run_select_statement(f"SELECT u.id, u.email, u.username, u.password, u.bio, u.birthdate, u.image_url, u.banner_url FROM users AS u INNER JOIN login AS l ON l.user_id = u.id WHERE l.{column} = ?", [token, ])
    return user_info[0]