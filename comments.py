from bsmodel import *


def add_comment(cursor,conn,comment:COMMENT):
    sql = ""
    cursor.execute(sql)
    new_comment = cursor.fetchone()
    conn.commit()
    return{'data': new_comment}

def get_comments(cursor):
    cursor.execute("""SELECT * FROM Comment """)
    allComments = cursor.fetchall()
    return{"data":allComments}

def edit_comment(cursor,comment:COMMENT):
    return 0