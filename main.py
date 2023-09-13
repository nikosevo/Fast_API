from fastapi import  FastAPI,Response, status, HTTPException

import connect
from datetime import date
from bsmodel import *
from comments import *

import comments


app = FastAPI()

conn = connect.create_connection(r"newsreport.db")
cursor= conn.cursor()


@app.get("/")
def root():

    return {"message": "Go to /docs to see the API documentation"}


@app.get("/articles")
def get_posts():
    cursor.execute("""SELECT * FROM Articles """)
    allnews = cursor.fetchall()
    return{"data":allnews}

@app.post('/articles',status_code=status.HTTP_201_CREATED)
def add_article(article: ARTICLE):
    today = date.today()
    str_date = today.strftime("%m/%d/%Y")
    sql = "INSERT INTO Articles(title,content,creation_date,topic_id) VALUES (\"{}\",\"{}\",\"{}\",{})".format(article.title,article.content,str_date,article.topic)
    print(sql)
    cursor.execute(sql)
    new_article = cursor.fetchone()

    conn.commit()

    return{'data': new_article}

@app.put('/articles/{id}/submit',status_code=status.HTTP_200_OK)
def submit_article(id: int):

    #if not publisehd
    sql = "SELECT state FROM Articles WHERE article_id = \"{}\" ".format (str(id))
    print(sql)
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
        new_article = cursor.fetchone()

        conn.commit()

        return{'data': new_article}

@app.put('/articles/{id}/deny',status_code=status.HTTP_200_OK)
def deny_article(id: int,reason:str):

    #if not publisehd
    sql = "SELECT state FROM Articles WHERE article_id = \"{}\" ".format (str(id))
    print(sql)
    cursor.execute(sql)
    state = cursor.fetchone()

    if not state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"article with id {id} was not found")

    
    #then change those things: title , content, topics
    if(state[0] == 1):
        sql = "UPDATE Articles SET state = 0 , rejected = \"{}\" WHERE article_id = \"{}\" RETURNING * ".format(reason,id)
        print(sql)
        cursor.execute(sql)
        new_article = cursor.fetchone()

        conn.commit()

        return{'data': new_article}


@app.put('/articles/{id}/accept',status_code=status.HTTP_200_OK)
def accept_article(id: int):

    #if not publisehd
    sql = "SELECT state FROM Articles WHERE article_id = \"{}\" ".format (str(id))
    print(sql)
    cursor.execute(sql)
    state = cursor.fetchone()

    if not state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"article with id {id} was not found")

    
    #then change those things: title , content, topics
    if(state[0] == 1):
        sql = "UPDATE Articles SET state = 2 WHERE article_id = \"{}\" RETURNING * ".format(id)
        print(sql)
        cursor.execute(sql)
        new_article = cursor.fetchone()

        conn.commit()

        return{'data': new_article}
    

@app.put('/articles/{id}/publish',status_code=status.HTTP_200_OK)
def accept_article(id: int):

    #if not publisehd
    sql = "SELECT state FROM Articles WHERE article_id = \"{}\" ".format (str(id))
    print(sql)
    cursor.execute(sql)
    state = cursor.fetchone()

    if not state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"article with id {id} was not found")

    
    #then change those things: title , content, topics
    if(state[0] == 2):
        sql = "UPDATE Articles SET state = 3 WHERE article_id = \"{}\" RETURNING * ".format(id)
        print(sql)
        cursor.execute(sql)
        new_article = cursor.fetchone()

        conn.commit()

        return{'data': new_article}

@app.put('/articles/{id}',status_code=status.HTTP_200_OK)
def modify_article(id: int , article: ARTICLE):

    #if not publisehd
    sql = "SELECT state FROM Articles WHERE article_id = \"{}\" ".format (str(id))
    print(sql)
    cursor.execute(sql)
    state = cursor.fetchone()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"article with id {id} was not found")

    
    #then change those things: title , content, topics
    print(state[0])
    if(state[0] != 3):
        sql = "UPDATE Articles SET title = \"{}\", content = \"{}\",topic_id = {} WHERE article_id = \"{}\" RETURNING * ".format(article.title,article.content,article.topic,id)
        print(sql)
        cursor.execute(sql)
        new_article = cursor.fetchone()

        conn.commit()

        return{'data': new_article}

@app.get("/articles/search/{keyword}")
def get_article(keyword: str):

    cursor.execute("SELECT * FROM Articles WHERE title LIKE '%" + keyword + "%' OR content LIKE '%" + keyword + "%'")
    
    article = cursor.fetchone()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"article with id {id} was not found")
    return {"article ": article}

@app.get("/articles/{id}")
def get_article(id: int):

    cursor.execute("SELECT * FROM Articles WHERE article_id = \"{}\" ".format (str(id)))
    
    article = cursor.fetchone()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"article with id {id} was not found")
    return {"article ": article}


@app.delete("/articles/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_dvd(id: int):
    cursor.execute()
    deleted_article = cursor.fetchone()
    conn.commit()
    if deleted_article == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"article with id {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


app.get("/comments")
get_comments(cursor)
