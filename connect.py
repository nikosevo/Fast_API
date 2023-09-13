import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to database ")
        return conn
    except Error as e:
        print("Connecting to database failed!")
        print("Error: ", e)
    

