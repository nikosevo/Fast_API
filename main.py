from fastapi import  FastAPI,Response, status, HTTPException

import connect
from bsmodel import *

import articles as art
import comments as com
import topics as top

app = FastAPI()

conn = connect.create_connection(r"newsreport.db")
cursor= conn.cursor()


@app.get("/")
def root():

    return {"message": "Go to /docs to see the API documentation"}


#### ARTICLE FUCNTIONS ==================================

@app.get("/articles")
def get_posts():
    return art.get_posts(cursor)

@app.post('/articles',status_code=status.HTTP_201_CREATED)
def add_article(article: ARTICLE):
    return art.get_article(cursor,conn,article)

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
    return art.accept_article(cursor,conn,id)

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
def add_comment(comment: COMMENT):
    return com.add_comment(cursor,conn,comment)

@app.put('/articles/{id}/comments/{comment_id}/accept',status_code=status.HTTP_200_OK)
def accept_comment(comment: COMMENT):
    return 0

@app.put('/articles/{id}/comments/{comment_id}/reject',status_code=status.HTTP_200_OK)
def reject_comment(comment: COMMENT):
    return 0

@app.put('/articles/{id}/comments/{comment_id}',status_code=status.HTTP_200_OK)
def edit_comment(comment: COMMENT):
    return com.edit_comment(cursor,comment)


#### TOPICS FUNCTION =================================

@app.get('/topics',status_code=status.HTTP_200_OK)
def get_topics(role:str):
    return 0

@app.get('/topics/{topic_id}',status_code=status.HTTP_200_OK)
def get_topic(topic_id):
    return 0

@app.post('/topics',status_code=status.HTTP_201_CREATED)
def add_topic(topic: TOPIC):
    return top.add_topic(cursor,conn,topic)

@app.put('/topics/{topic_id}/accept',status_code=status.HTTP_200_OK)
def edit_topic(topic: TOPIC):
    return 0

@app.put('/topics/{topic_id}/reject',status_code=status.HTTP_200_OK)
def reject_topic(topic: TOPIC):
    return 0

@app.put('/topics/{topic_id}',status_code=status.HTTP_200_OK)
def edit_topic(topic: TOPIC):
    return 0

@app.get("/topics/search/{keyword}")
def search_topic(keyword: str):
    return top.search_topic(cursor,keyword)

