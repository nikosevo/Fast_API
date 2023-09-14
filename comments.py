from bsmodel import *
from datetime import date
from fastapi import  FastAPI,Response, status, HTTPException



def get_comments(cursor,article_id):
    cursor.execute("SELECT * FROM Comment WHERE article_id = \"{}\" ORDER BY creation_date ASC".format(str(article_id)))
    allComments = cursor.fetchall()
    return{"data":allComments}

def add_comment(cursor,conn,article_id,comment:COMMENT):
    today = date.today()
    str_date = today.strftime("%m/%d/%Y")
    sql = "INSERT INTO Comment(content,creation_date,username,article_id)VALUES (\"{}\",\"{}\",\"{}\",{})".format(comment.content,str_date,comment.username,article_id)
    cursor.execute(sql)
    new_comment = cursor.fetchone()
    conn.commit()
    return{'data': new_comment}

def accept_comment(cursor,conn,id:int):

    sql = "UPDATE Comment SET state = 1 WHERE comment_id = \"{}\" RETURNING * ".format(str(id))
    print(sql)
    cursor.execute(sql)
    co = cursor.fetchone()

    conn.commit()

    return{'data': co}

def edit_comment(cursor,conn,comment_id,comment:COMMENT):
    
    #then change those things: content
    sql = "UPDATE Comment SET content = \"{}\" WHERE comment_id = \"{}\" RETURNING * ".format(comment.content,comment_id)
    print(sql)
    cursor.execute(sql)
    co = cursor.fetchone()

    conn.commit()

    return{'data': co}

def reject_comment(cursor,conn,comment_id):
    sql = "DELETE FROM Comment WHERE comment_id = \"{}\" RETURNING * ".format(str(comment_id))
    cursor.execute(sql)
    co = cursor.fetchone()

    conn.commit()

    return{'data': co}

