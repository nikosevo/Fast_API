from fastapi import  FastAPI,Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import connect


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ARTICLE(BaseModel):
    title: str
    topic: str
    content: str

class COMMENT(BaseModel):
    username: Optional[str] = None
    content:str


conn = connect.create_connection(r"newsreport.db")
cursor= conn.cursor()



@app.get("/")
def root():

    return {"message": "Go to /docs to see the API documentation"}


@app.get("/articles")
def get_posts():
    cursor.execute("""SELECT * FROM news """)
    allnews = cursor.fetchall()
    return{"data":allnews}


@app.post('/articles',status_code=status.HTTP_201_CREATED)
def add_article(article: ARTICLE):
    cursor.execute()
    new_articles = cursor.fetchone()

    conn.commit()

    return{'data': new_articles}

@app.get("/articles/{id}")
def get_article(id: int):
    cursor.execute("""SELECT * FROM articles WHERE id = %s """, (str(id),))
    
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


