from fastapi.testclient import TestClient
from main import app
import pytest
client = TestClient(app)


def test_login_user():
    res = client.post("/login", json={"username": "nikosevo", "password": "123"})
    print(res.json().get('detail'))
    assert res.json().get('detail') == "logged in as nikosevo"
    assert res.status_code == 202

#-----------------TOPICS-------------------------------------------------------

@pytest.mark.parametrize("topic_name", [
    "Technology",
    "Science",
    "Sports",
])

def test_add_topic(topic_name):
    res = client.post(
        "/topics", json={"name": topic_name})
    assert res.status_code == 201
def test_get_topics():
    res = client.get("/topics")
    assert res.status_code == 200

def test_get_topic():
    res = client.get("/topics/1")
    assert res.status_code == 200



def test_edit_topic():
    res = client.put("/topics/1", json={"name": "Edited Topic Name"})
    assert res.status_code == 200

def test_accept_topic():
    res = client.put("/topics/1/accept")
    assert res.status_code == 200

def test_reject_topic():
    res = client.put("/topics/1/reject")
    assert res.status_code == 200

def test_search_topic():
    res = client.get("/topics/search/Technology")
    assert res.status_code == 200

def test_view_articles_on_topic():
    res = client.get("/topics/Technology/articles")
    assert res.status_code == 200

#-----------------ARTICLES-----------------------------------------------------
@pytest.mark.parametrize("title, topic, content", [
    ("awesome new title", 1, "awesome new content"),
    ("favorite pizza", 2, "i love pepperoni"),
    ("tallest skyscrapers", 3, "niko's house"),
])
def test_add_article(title, topic, content):
    res = client.post(
        "/articles", json={  "title": title,  "topic": topic,  "content": content})
    assert res.json().get('data')[1]== title
    assert res.json().get('data')[5]== topic
    assert res.json().get('data')[2]== content

    assert res.status_code == 201

def test_submit_article():
    res = client.put("/articles/1/submit")
    assert res.status_code == 200

def test_deny_article():
    res = client.put("/articles/1/deny", json={"reason": "Some reason"})
    assert res.status_code == 200

def test_accept_article():
    res = client.put("/articles/1/accept")
    assert res.status_code == 200

def test_modify_article():
    article_data = {"title": "Modified Title","topic":2, "content": "Modified Content"}
    res = client.put("/articles/1", json=article_data)
    assert res.status_code == 200

def test_publish_article():
    res = client.put("/articles/1/publish")
    assert res.status_code == 200

def test_search_article():
    res = client.get("/articles/search/content")
    assert res.status_code == 200


def test_delete_article():
    res = client.delete("/articles/2")
    assert res.status_code == 204

def test_get_article_topic():
    res = client.get("/articles/1")
    assert res.status_code == 200


#-------------------COMMENT TESTING------------

@pytest.mark.parametrize("comment_text", [
    "This is a great article!",
    "I disagree with some points.",
    "Nice job on this one!",
])
def test_add_comment(comment_text):
    res = client.post(
        "/articles/1/comments", json={"comment": comment_text})
    assert res.status_code == 201

def test_edit_comment():
    comment_data = {"comment": "Edited Comment Text"}
    res = client.put("/articles/1/comments/1", json=comment_data)
    assert res.status_code == 200


def test_accept_comment():
    res = client.put("/articles/1/comments/1/accept")
    assert res.status_code == 200

def test_get_comment():
    res = client.get("/articles/1/comments")
    assert res.status_code == 200

def test_reject_comment():
    res = client.put("/articles/1/comments/1/reject")
    assert res.status_code == 200

#--------------UNAUTHORIZED----------------------------------

def test_logout_user():
    res = client.post("/logout")
    
    assert res.json().get('detail') == "Successfully logged out"
    assert res.status_code == 200

def test_unauth_user_add_article():
    res = client.post(
        "/articles", json={  "title": "title",  "topic": 1,  "content": "content"})
    
    assert res.json().get('detail') == "Access Denied"
    assert res.status_code == 401

def test_unauth_user_submit_article():
    res = client.put("/articles/1/submit")
    assert res.status_code == 401

def test_unauth_user_deny_article():
    res = client.put("/articles/1/deny", json={"reason": "Some reason"})
    assert res.status_code == 401

def test_unauth_user_accept_article():
    res = client.put("/articles/1/accept")
    assert res.status_code == 401

def test_unauth_user_modify_article():
    article_data = {"title": "Modified Title","topic":2, "content": "Modified Content"}
    res = client.put("/articles/1", json=article_data)
    assert res.status_code == 401

def test_unauth_user_publish_article():
    res = client.put("/articles/1/publish")
    assert res.status_code == 401

def test_unauth_user_delete_article():
    res = client.delete("/articles/1")
    assert res.status_code == 401
