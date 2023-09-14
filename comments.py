from bsmodel import *

def get_comments(cursor):
    cursor.execute("""SELECT * FROM Comment """)
    allComments = cursor.fetchall()
    return{"data":allComments}

def edit_comments(cursor,comment:COMMENT):
    return 0