import connect


conn = connect.create_connection(r"newsreport.db")


sql = """ CREATE TABLE IF NOT EXISTS User (
                                        username text PRIMARY KEY,
                                        password text NOT NULL,
                                        full_name text,
                                        role integer
                                    ); """
c = conn.cursor()
c.execute(sql)