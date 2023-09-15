from fastapi import  FastAPI,Response, status, HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated

import connect
from bsmodel import *

import articles as art
import comments as com
import topics as top

def refresh_db():
    #UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='Comment';
    sql = "DELETE FROM \"Topic\""
    cursor.execute(sql)
    sql = "DELETE FROM \"Articles\""
    cursor.execute(sql)
    sql = "DELETE FROM \"Comment\""
    cursor.execute(sql)


    sql = "UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME=\"Topic\""
    cursor.execute(sql)
    sql = "UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME=\"Articles\""
    cursor.execute(sql)
    sql = "UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME=\"Comment\""
    cursor.execute(sql)


app = FastAPI()

conn = connect.create_connection(r"newsreport.db")
cursor= conn.cursor()

app.logged_role = 0

## role = 0 : guess
## role = 1 : writter 
## role = 2 : admin 

@app.get("/")
def root():

    return {"message": "Go to /docs to see the API documentation"}

#### AUTHENTICATION =====================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/login",status_code=status.HTTP_202_ACCEPTED)
async def login(user:USER):
    sql = "SELECT username,password,role FROM User WHERE username = \"{}\"".format(user.username,user.password)
    cursor.execute(sql)
    user_data = cursor.fetchone()

    if(user_data[1] == user.password and user_data[0] == user.username):
        app.logged_role = int(user_data[2])
        return {'detail':"logged in as {}".format(user.username)}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN
                            ,detail=f"wrong credentials")
@app.post("/loggout")
def logout():
    app.logged_role = 0
    return{'detail':"Successfully logged out"}

#### ARTICLE FUCNTIONS ==================================

@app.get("/articles")
def get_posts():
    return art.get_posts(cursor,app.logged_role)

@app.post('/articles',status_code=status.HTTP_201_CREATED)
def add_article(article: ARTICLE):
    if(app.logged_role > 0 ):
        return art.add_article(cursor,conn,article)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")
@app.put('/articles/{id}/submit',status_code=status.HTTP_200_OK)
def submit_article(id: int):
    if(app.logged_role > 0 ):
        return art.submit_article(cursor,conn,id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")
        

@app.put('/articles/{id}/deny',status_code=status.HTTP_200_OK)
def deny_article(id: int,denied:DENIED):
    if(app.logged_role == 2 ):
        return art.deny_article(cursor,conn,id,denied)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")
@app.put('/articles/{id}/accept',status_code=status.HTTP_200_OK)
def accept_article(id: int):
    if(app.logged_role == 2 ):
        return art.accept_article(cursor,conn,id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")    
@app.put('/articles/{id}/publish',status_code=status.HTTP_200_OK)
def publish_article(id: int):
    if(app.logged_role == 2 ):
        return art.publish_article(cursor,conn,id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")
@app.put('/articles/{id}',status_code=status.HTTP_200_OK)
def modify_article(id: int , article: ARTICLE):
    if(app.logged_role > 0 ):
        return art.modify_article(cursor,conn,id,article)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")
@app.get("/articles/search/{keyword}")
def search_article(keyword: str):
    return art.search_article(cursor,keyword)

@app.get("/articles/{id}")
def get_article(id: int):
    return art.get_article(cursor,conn,id)

@app.delete("/articles/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id: int):
    if(app.logged_role == 2 ):
        return art.delete_article(cursor,conn,id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")
@app.get("/articles/{topic_id}")
def get_article(topic_id: int):
    return art.get_article_topic(cursor,conn,topic_id)

#### COMMENT FUNCTION =================================



@app.post('/articles/{id}/comments',status_code=status.HTTP_201_CREATED)
def add_comment(id:int,comment: COMMENT):
    return com.add_comment(cursor,conn,id,comment)

@app.get('/articles/{id}/comments',status_code=status.HTTP_200_OK)
def get_comment(id:int):
    return com.get_comments(cursor,conn,id)

@app.put('/articles/{id}/comments/{comment_id}/accept',status_code=status.HTTP_200_OK)
def accept_comment(comment_id:int):
    if(app.logged_role == 2 ):
        return com.accept_comment(cursor,conn,comment_id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")
@app.put('/articles/{id}/comments/{comment_id}/reject',status_code=status.HTTP_200_OK)
def reject_comment(comment_id:int):
    if(app.logged_role == 2 ):
        return com.reject_comment(cursor,conn,comment_id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")
@app.put('/articles/{id}/comments/{comment_id}',status_code=status.HTTP_200_OK)
def edit_comment(id:int, comment: COMMENT):
    if(app.logged_role == 2 ):
        return com.edit_comment(cursor,conn,id,comment)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")

#### TOPICS FUNCTION =================================

###### fix that !!!!!!
@app.get('/topics',status_code=status.HTTP_200_OK)
def get_topics():
    return top.get_topics(cursor,conn,app.logged_role)

@app.get('/topics/{topic_id}',status_code=status.HTTP_200_OK)
def get_topic(topic_id):
    return top.get_topic(cursor,conn,topic_id)

@app.post('/topics',status_code=status.HTTP_201_CREATED)
def add_topic(topic: TOPIC):
    if(app.logged_role > 0 ):
        return top.add_topic(cursor,conn,topic)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")
@app.put('/topics/{topic_id}/accept',status_code=status.HTTP_200_OK)
def accept_topic(topic_id:int):
    if(app.logged_role > 0 ):
        return top.accept_topic(cursor,conn,topic_id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")
@app.put('/topics/{topic_id}/reject',status_code=status.HTTP_200_OK)
def reject_topic(topic_id:int):
    if(app.logged_role == 2 ):
        return top.reject_topic(cursor,conn,topic_id)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")
@app.put('/topics/{topic_id}',status_code=status.HTTP_200_OK)
def edit_topic(topic_id:int,topic: TOPIC):
    if(app.logged_role > 0 ):
        return top.edit_topic(cursor,conn,topic_id,topic)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Access Denied")
@app.get('/topics/search/{keyword}',status_code=status.HTTP_200_OK)
def search_topic(keyword: str):
    return top.search_topic(cursor,keyword)

@app.get('/topics/{keyword}/articles',status_code=status.HTTP_200_OK)
def view_articles_on_topic(keyword:str):
    return top.view_articles_on_topic(cursor,conn,keyword)

