from bsmodel import *

def get_comments(cursor):
    cursor.execute("""SELECT * FROM Comment """)
    allComments = cursor.fetchall()
    return{"data":allComments}

def add_comment(cursor,conn,comment:COMMENT):
    sql = "INSERT INTO Comment(content,creation_date,username,article_id)VALUES (\"{}\",\"{}\",\"{}\",{})".format(1,2,3,4)
    cursor.execute(sql)
    new_comment = cursor.fetchone()
    conn.commit()
    return{'data': new_comment}

def submit_comment(cursor,comment:COMMENT):

    return {'data': new_comment}

def edit_comment(cursor,comment:COMMENT):
    return 0