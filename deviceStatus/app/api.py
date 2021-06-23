from fastapi import FastAPI, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.model import DeviceStatusSchema
from app.auth.auth_handler import JWT_SECRET, JWT_ALGORITHM
from app.auth.auth_bearer import JWTBearer
from app.db import DB
from typing import Optional
import jwt


posts = []  # DB 대신 쓰는 배열
deviceDatas = []
devices = []

app = FastAPI()
mydb = DB()

origins = ["http://localhost", "http://localhost:3000",
           "http://localhost:8000", "http://localhost:8080", "http://localhost:9000",
           "https://localhost", "https://localhost:3000",
           "https://localhost:8000", "https://localhost:8080", "https://localhost:9000",
           "localhost", "localhost:3000",
           "localhost:8000", "localhost:8080", "localhost:9000", "192.168.0.1", '*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE', 'OPTIONS'],
    allow_headers=["*"],
)


def check_db(mydb):
    if mydb.checkDB():
        mydb = DB()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    check_db(mydb)
    item = {"message": "WORKING !!!"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=item)


@ app.post("/deviceData", tags=["deviceData"])
async def add_data(deviceData: DeviceStatusSchema) -> dict:
    check_db(mydb)
    try:
        lastStatus = mydb.getDeviceStatusBySerial(deviceData.deviceSerial)
        statusDiction = ["deviceSerial", "longitude", "latitude", "temp",
                         "accelMax", "heartRate", "batteryLevel", "critical", "button"]
        lastStatus = lastStatus[1:]
        lastStatus = dict(zip(statusDiction, lastStatus))
        deviceData2 = dict(deviceData)
        del deviceData2['id']
        deviceData2['longitude'] = round(deviceData2['longitude'], 3)
        deviceData2['latitude'] = round(deviceData2['latitude'], 3)
        deviceData2['accelMax'] = round(deviceData2['accelMax'], 3)
        lastStatus['longitude'] = round(lastStatus['longitude'], 3)
        lastStatus['latitude'] = round(lastStatus['latitude'], 3)
        lastStatus['accelMax'] = round(lastStatus['accelMax'], 3)
        if(deviceData2 == lastStatus):
            deviceData.critical = 3
    except TypeError:
        None
    mydb.addDeviceStatus(deviceData)
    item = {
        "data": "deviceData added."
    }
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)


@ app.get("/deviceData", dependencies=[Depends(JWTBearer())], tags=["deviceData"])
async def get_deviceData_list(Authorization: Optional[str] = Header(None)):
    check_db(mydb)
    token = Authorization[7:]
    user_id = jwt.decode(token, JWT_SECRET, algorithms=[
                         JWT_ALGORITHM])["user_id"]
    devicestatus = mydb.getDeviceStatus(user_id)
    statusList = []
    statusList2 = []
    statusDiction = ["deviceName", "longitude", "latitude", "temp",
                     "accelMax", "heartRate", "batteryLevel", "critical", "button"]
    for tuple in devicestatus:
        try:
            statusList.append(list(tuple))
        except TypeError:
            statusList.append(None)
    for stat in statusList:
        try:
            del stat[0]
            temp = stat
            device = mydb.getDeviceSingle(temp[0])
            temp[0] = device[2]
            statusList2.append(dict(zip(statusDiction, temp)))
        except TypeError:
            None
    item = {
        "data": statusList2
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=item)
