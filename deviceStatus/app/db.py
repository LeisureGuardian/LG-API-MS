import pymysql
from app.model import DeviceStatusSchema


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
        DB.sql = "CREATE TABLE IF NOT EXISTS deviceTable(id int NOT NULL AUTO_INCREMENT, deviceSerial int, deviceName char(30), organization char(30), addedDate char(10), PRIMARY KEY(deviceSerial), UNIQUE(id))"
        DB.cur.execute(DB.sql)
        DB.conn.commit()
        DB.sql = "CREATE TABLE IF NOT EXISTS deviceStatusTable(id int NOT NULL AUTO_INCREMENT, deviceSerial int, longtitude float, latitude float, temp float, accelMax float, heartRate int, batteryLevel int, critical int, button int, PRIMARY KEY(id))"
        DB.cur.execute(DB.sql)
        DB.conn.commit()

    def __del__(self):
        DB.conn.close()

    def addDeviceStatus(self, status: DeviceStatusSchema):

        DB.sql = "INSERT INTO deviceStatusTable(deviceSerial, longtitude, latitude, temp, accelMax, heartRate, batteryLevel, critical, button) VALUES('" + str(status.deviceSerial) + "', '" + str(status.longitude) + \
            "', '" + str(status.latitude) + "', '" + str(status.temp) + "', '" + str(status.accelMax) + "', '" + str(status.heartRate) + \
            "', '" + str(status.batteryLevel) + "', '" + \
            str(status.critical) + "', '" + str(status.button) + "')"
        # print(DB.sql)
        DB.cur.execute(DB.sql)
        DB.conn.commit()

    def getDeviceStatus(self, email):

        row = DB.getDeviceAll(self, email)
        list = []
        for device in row:
            DB.sql = "SELECT * FROM deviceStatusTable WHERE deviceSerial='" + \
                str(device[1]) + "' ORDER BY id DESC limit 1"
            DB.cur.execute(DB.sql)
            list.append(DB.cur.fetchone())
        return list

    def getDeviceStatusBySerial(self, serial):
        DB.sql = "SELECT * From deviceStatusTable WHERE deviceSerial='" + \
            str(serial) + "' ORDER BY id DESC limit 1"
        DB.cur.execute(DB.sql)
        data = DB.cur.fetchone()
        return data

    def checkDB(self):
        try:
            DB.sql = "SHOW DATABASES"
            DB.cur.execute(DB.sql)
        except pymysql.err.InterfaceError:
            return True
        return False
