from bsmodel import *
from datetime import date
from fastapi import  FastAPI,Response, status, HTTPException



def get_comments(cursor,id):
    cursor.execute("SELECT * FROM Comment WHERE comment_id = \"{}\" ORDER BY creation_date ASC".format(str(id)))
    allComments = cursor.fetchall()
    return{"data":allComments}

def add_comment(cursor,conn,username,content,article_id,comment:COMMENT):
    today = date.today()
    str_date = today.strftime("%m/%d/%Y")
    sql = "INSERT INTO Comment(content,creation_date,username,article_id)VALUES (\"{}\",\"{}\",\"{}\",{})".format(content,str_date,username,article_id)
    cursor.execute(sql)
    new_comment = cursor.fetchone()
    conn.commit()
    return{'data': new_comment}

def accept_comment(cursor,conn,id:int):

    #if not publisehd
    sql = "SELECT state FROM Comment WHERE comment_id = \"{}\" ".format (str(id))
    cursor.execute(sql)
    state = cursor.fetchone()

    if not state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"article with id {id} was not found")

    
    #then change those things: title , content, topics
    if(state[0] == 0):
        sql = "UPDATE Articles SET state = 1 WHERE article_id = \"{}\" RETURNING * ".format(id)
        print(sql)
        cursor.execute(sql)
        co = cursor.fetchone()

        conn.commit()

        return{'data': co}


def edit_comment(cursor,comment:COMMENT):
    return 0