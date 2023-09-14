from bsmodel import *
from datetime import date


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
    

    if(state[0] != 1):
        sql = "DELETE FROM Topic WHERE topic_id = \"{}\" RETURNING * ".format(str(topic_id))
        cursor.execute(sql)
        co = cursor.fetchone()

        conn.commit()

        return{'data': co}