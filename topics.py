from bsmodel import *
from datetime import date
from fastapi import  FastAPI,Response, status, HTTPException



def get_topics(cursor,conn,role):
    print(role)
    if(int(role) == 2):
        print("hi")
        sql = "SELECT * FROM Topic"
        cursor.execute(sql)
        to = cursor.fetchall()
        return{"data":to}
    else:
        sql = "SELECT * FROM Topic WHERE state = 1"
        cursor.execute(sql)
        topics = cursor.fetchall()
        return{"data":topics}
def get_topic(cursor,conn,topic_id):
    sql = "SELECT * FROM Topic WHERE topic_id = \"{}\"".format(str(topic_id))
    cursor.execute(sql)
    to = cursor.fetchone()
    return{"data":to}

def edit_topic(cursor,conn,topic_id,topic:TOPIC):
    sql = "UPDATE Topic SET name = \"{}\" WHERE topic_id = \"{}\" RETURNING * ".format(topic.topic_name , str(topic_id))
    cursor.execute(sql)
    topic = cursor.fetchone()
    conn.commit()
    return{'data': topic}



def add_topic(cursor,conn,topic:TOPIC):
    today = date.today()
    str_date = today.strftime("%m/%d/%Y")
    if(topic.parentTopic == None):
            sql = "INSERT INTO Topic(name,creation_date)VALUES (\"{}\",\"{}\")".format(topic.topic_name,str_date)
    else:
        sql = "INSERT INTO Topic(name,creation_date,parent_topic_id)VALUES (\"{}\",\"{}\",{})".format(topic.topic_name,str_date,topic.parentTopic)
    cursor.execute(sql)
    topic = cursor.fetchone()
    conn.commit()
    return{'data': topic}

def accept_topic(cursor,conn,topic_id):
    sql = "UPDATE Topic SET state = 1 WHERE topic_id = \"{}\" RETURNING * ".format(str(topic_id))
    cursor.execute(sql)
    topic = cursor.fetchone()
    conn.commit()
    return{'data': topic}

def reject_topic(cursor,conn,topic_id):
    sql = "SELECT state FROM Topic WHERE topic_id = \"{}\" ".format (str(topic_id))
    print(sql)
    cursor.execute(sql)
    state = cursor.fetchone()
    
    if not state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"topic with id {id} was not found")
    if(state[0] != 1):
        sql = "DELETE FROM Topic WHERE topic_id = \"{}\" RETURNING * ".format(str(topic_id))
        cursor.execute(sql)
        co = cursor.fetchone()

        conn.commit()

        return{'data': co}
    
def search_topic(cursor,keyword):
    cursor.execute("SELECT * FROM Topic WHERE name LIKE '%" + keyword + "%'")
    
    article = cursor.fetchone()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"article with id {id} was not found")
    return {"article ": article}

def view_articles_on_topic(cursor,conn,keyword):
    print(keyword)
    if(keyword.isdigit()):
        sql = "SELECT content from Articles WHERE topic_id = {}".format(keyword)
    else:
        sql = "SELECT content from Articles INNER JOIN Topic ON Articles.topic_id = Topic.topic_id WHERE Topic.name = \"{}\"".format(keyword)
    cursor.execute(sql)
    allArt = cursor.fetchall()
    return{"data":allArt}