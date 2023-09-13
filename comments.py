
def get_comments(cursor):
    cursor.execute("""SELECT * FROM Comment """)
    allComments = cursor.fetchall()
    return{"data":allComments}