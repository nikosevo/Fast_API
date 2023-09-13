from fastapi import  FastAPI,Response, status, HTTPException

import connect
from datetime import date
from bsmodel import *


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


