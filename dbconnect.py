
import mariadb
import dbcreds
import traceback


def get_db_connection():
    # Create connection to the DB and return it as true if success
    try:
        return mariadb.connect(user=dbcreds.user, password=dbcreds.password,
                               host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    except:
        print("Error connecting to DB!")
        traceback.print_exc()
        return None


def get_db_cursor(conn):
    # Get the cursor of the connection and return it as true if success
    try:
        return conn.cursor()
    except:
        print("Error creating cursor on DB!")
        traceback.print_exc()
        return None


def close_db_cursor(cursor):
    # Close the cursor
    if(cursor == None):
        return True
    try:
        cursor.close()
        return True
    except:
        print("Error closing cursor on DB!")
        traceback.print_exc()
        return False


def close_db_connection(conn):
    # Close the connection
    if(conn == None):
        return True
    try:
        conn.close()
        return True
    except:
        print("Error closing connection to DB!")
        traceback.print_exc()
        return False
