import pymysql
from app.model import DeviceSchema


class DB:
    conn = None
    cur = None
    sql = ""

    def __init__(self):
        DB.conn = pymysql.connect(host='localhost', user='root',
                                  password='Nekarakube!1', db='LG', charset='utf8')
        DB.cur = DB.conn.cursor()
        DB.sql = "CREATE TABLE IF NOT EXISTS deviceTable(id int NOT NULL AUTO_INCREMENT, deviceSerial int, deviceName char(30), organization char(30), addedDate char(10), PRIMARY KEY(deviceSerial), UNIQUE(id))"
        DB.cur.execute(DB.sql)
        DB.conn.commit()

    def __del__(self):
        DB.conn.close()

    def addDevice(self, device: DeviceSchema):

        DB.sql = "INSERT INTO deviceTable(deviceSerial, deviceName, organization, addedDate) VALUES('" + str(
            device.deviceSerial) + "', '" + device.deviceName + "', '" + device.organization + "', '" + device.addedDate + "')"
        # print(DB.sql)
        DB.cur.execute(DB.sql)
        DB.conn.commit()

    def getDeviceAll(self, email):

        organization = DB.getOrganization(self, email)
        DB.sql = "SELECT * FROM deviceTable WHERE organization='" + organization + "'"
        # print(DB.sql)
        DB.cur.execute(DB.sql)
        row = DB.cur.fetchall()

        return row

    def getDeviceSingle(self, serial):

        DB.sql = "SELECT * FROM deviceTable WHERE deviceSerial='" + \
            str(serial) + "'"
        # print(DB.sql)
        DB.cur.execute(DB.sql)
        row = DB.cur.fetchone()

        return row

    def deleteDeviceSingle(self, serial):

        DB.sql = "DELETE FROM deviceTable WHERE deviceSerial='" + \
            str(serial) + "'"
        # print(DB.sql)
        DB.cur.execute(DB.sql)
        DB.conn.commit()

        return True

    def getOrganization(self, email):

        DB.sql = "SELECT organization FROM userTable WHERE email='" + email + "'"
        # print(DB.sql)
        DB.cur.execute(DB.sql)
        row = DB.cur.fetchone()
        return row[0]

    def checkDB(self):
        try:
            DB.sql = "SHOW DATABASES"
            DB.cur.execute(DB.sql)
        except pymysql.err.InterfaceError:
            return True
        return False
