import connect


conn = connect.create_connection(r"newsreport.db")

sql = "SELECT * from User"

cur = conn.cursor()
cur.execute(sql)

rows = cur.fetchall()

for row in rows:
    print(row)

