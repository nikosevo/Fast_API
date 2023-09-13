import connect


conn = connect.create_connection(r"newsreport.db")

sql = "SELECT * from Articles"

cur = conn.cursor()
cur.execute(sql)

rows = cur.fetchall()

for row in rows:
    print("hi"  + row)

