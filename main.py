from fastapi import  FastAPI,Response, status, HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated

import connect
from bsmodel import *

import articles as art
import comments as com
import topics as top


app = FastAPI()

conn = connect.create_connection(r"newsreport.db")
cursor= conn.cursor()

app.logged_role = 0

@app.get("/")
def root():

    return {"message": "Go to /docs to see the API documentation"}

#### AUTHENTICATION =====================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/login{username}/{password}")
async def login(username:str,password:str):
    sql = "SELECT username,password,role FROM User WHERE username = \"{}\"".format(username,password)
    cursor.execute(sql)
    user_data = cursor.fetchone()

    if(user_data[1] == password and user_data[0] == username):
        app.logged_role = int(user_data[2])
        return {"logged in as {}".format(username)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"wrong credentials")
@app.post("loggout")
def logout():
    app.logged_role = 0
    return{"Successfully logged out"}

#### ARTICLE FUCNTIONS ==================================

@app.get("/articles")
def get_posts():
    print(app.logged_role)
    if(app.logged_role == 2 ):
        print(app.logged_role)
        return art.get_posts(cursor)
    else:
        return {"access Denied"}

@app.post('/articles',status_code=status.HTTP_201_CREATED)
def add_article(article: ARTICLE):
    return art.add_article(cursor,conn,article)

@app.put('/articles/{id}/submit',status_code=status.HTTP_200_OK)
def submit_article(id: int):
    return art.submit_article(cursor,conn,id)

@app.put('/articles/{id}/deny',status_code=status.HTTP_200_OK)
def deny_article(id: int,reason:str):
    return art.deny_article(cursor,conn,id,reason)

@app.put('/articles/{id}/accept',status_code=status.HTTP_200_OK)
def accept_article(id: int):
    return art.accept_article(cursor,conn,id)
    
@app.put('/articles/{id}/publish',status_code=status.HTTP_200_OK)
def publish_article(id: int):
    return art.publish_article(cursor,conn,id)

@app.put('/articles/{id}',status_code=status.HTTP_200_OK)
def modify_article(id: int , article: ARTICLE):
    return art.modify_article(cursor,conn,id,article)

@app.get("/articles/search/{keyword}")
def search_article(keyword: str):
    return art.search_article(cursor,keyword)

@app.get("/articles/{id}")
def get_article(id: int):
    return art.get_article(cursor,conn,id)

@app.delete("/articles/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id: int):
    return art.delete_article(cursor,conn,id)


@app.get("/articles/{topic_id}")
def get_article(topic_id: int):
    return art.get_article_topic(cursor,conn,topic_id)

#### COMMENT FUNCTION =================================



@app.post('/articles/{id}/comments',status_code=status.HTTP_201_CREATED)
def add_comment(id:int,comment: COMMENT):
    return com.add_comment(cursor,conn,id,comment)

@app.get('/articles/{id}/comments',status_code=status.HTTP_200_OK)
def get_comment():
    return com.get_comment(cursor,conn,id)

@app.put('/articles/{id}/comments/{comment_id}/accept',status_code=status.HTTP_200_OK)
def accept_comment(comment_id:int):
    return com.accept_comment(cursor,conn,comment_id)

@app.put('/articles/{id}/comments/{comment_id}/reject',status_code=status.HTTP_200_OK)
def reject_comment(comment_id:int):
    return com.reject_comment(cursor,conn,comment_id)

@app.put('/articles/{id}/comments/{comment_id}',status_code=status.HTTP_200_OK)
def edit_comment(id:int, comment: COMMENT):
    return com.edit_comment(cursor,conn,id,comment)


#### TOPICS FUNCTION =================================

@app.get('/topics',status_code=status.HTTP_200_OK)
def get_topics(role:str):
    return top.get_topics(cursor,conn,role)

@app.get('/topics/{topic_id}',status_code=status.HTTP_200_OK)
def get_topic(topic_id):
    return top.get_topic(cursor,conn,topic_id)

@app.post('/topics',status_code=status.HTTP_201_CREATED)
def add_topic(topic: TOPIC):
    return top.add_topic(cursor,conn,topic)

@app.put('/topics/{topic_id}/accept',status_code=status.HTTP_200_OK)
def edit_topic(topic_id:int):
    return top.accept_topic(cursor,conn,topic_id)

@app.put('/topics/{topic_id}/reject',status_code=status.HTTP_200_OK)
def reject_topic(topic_id:int):
    return top.reject_topic(cursor,conn,topic_id)

@app.put('/topics/{topic_id}',status_code=status.HTTP_200_OK)
def edit_topic(topic_id:int,topic: TOPIC):
    return edit_topic(cursor,conn,topic_id,topic)

@app.get('/topics/search/{keyword}',status_code=status.HTTP_200_OK)
def search_topic(keyword: str):
    return top.search_topic(cursor,keyword)

@app.get('/topics/{keyword}/articles',status_code=status.HTTP_200_OK)
def view_articles_on_topic(keyword:str):
    return top.view_articles_on_topic(cursor,conn,keyword)

