import pymysql
from app.model import UserSchema, UserLoginSchema


class DB:
    conn = None
    cur = None
    sql = ""

    def __init__(self):
        DB.conn = pymysql.connect(host='localhost', user='root',
                                  password='Nekarakube!1', db='LG', charset='utf8')
        DB.cur = DB.conn.cursor()
        DB.sql = "CREATE TABLE IF NOT EXISTS userTable(id int NOT NULL AUTO_INCREMENT, email char(30), password char(30), fullname char(30), organization char(30), PRIMARY KEY (email), UNIQUE(id))"
        DB.cur.execute(DB.sql)
        DB.conn.commit()

    def __del__(self):
        DB.conn.close()

    def addUser(self, user: UserSchema):

        DB.sql = "INSERT INTO userTable(email, password, fullname, organization) VALUES('" + user.email + \
            "', '" + user.password + "', '" + user.fullname + "', '" + user.organization + "')"
        # print(DB.sql)
        DB.cur.execute(DB.sql)
        DB.conn.commit()

    def getUser(self, user: UserLoginSchema):

        DB.sql = "SELECT * FROM userTable WHERE email='" + user.email + "'"
        # print(DB.sql)
        DB.cur.execute(DB.sql)
        row = DB.cur.fetchone()

        return row

    def checkDB(self):
        try:
            DB.sql = "SHOW DATABASES"
            DB.cur.execute(DB.sql)
        except pymysql.err.InterfaceError:
            return True
        return False
