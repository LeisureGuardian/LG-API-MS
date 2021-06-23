from fastapi import FastAPI, Body, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.model import PostSchema, UserSchema, UserLoginSchema, DeviceStatusSchema, DeviceSchema
from app.auth.auth_handler import signJWT, JWT_SECRET, JWT_ALGORITHM
from app.auth.auth_bearer import JWTBearer
from app.db import DB
import datetime
from typing import Optional
import jwt
import pymysql


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


def check_user(data: UserLoginSchema):
    dbUser = mydb.getUser(data)
    try:
        if dbUser[2] == data.password:
            return True
    except TypeError:
        return False
    return False


@app.get("/", tags=["root"])
async def read_root() -> dict:
    check_db(mydb)
    item = {"message": "WORKING !!!"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=item)


@app.post("/device", dependencies=[Depends(JWTBearer())], tags=["device"])
async def add_device(device: DeviceSchema, Authorization: Optional[str] = Header(None)) -> dict:
    check_db(mydb)
    token = Authorization[7:]
    user_id = jwt.decode(token, JWT_SECRET, algorithms=[
                         JWT_ALGORITHM])["user_id"]
    organization = mydb.getOrganization(user_id)
    device.organization = organization
    now = datetime.datetime.now()
    nowstr = "%04d%02d%02d" % (now.year, now.month, now.day)
    device.addedDate = nowstr
    try:
        mydb.addDevice(device)
    except pymysql.err.IntegrityError:
        item = {
            "error": "The device is already registered "
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=item)
    item = {
        "data": "device added."
    }
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)


@app.get("/device", dependencies=[Depends(JWTBearer())], tags=["device"])
async def get_device_list(Authorization: Optional[str] = Header(None)):
    check_db(mydb)
    token = Authorization[7:]
    user_id = jwt.decode(token, JWT_SECRET, algorithms=[
                         JWT_ALGORITHM])["user_id"]
    devices = mydb.getDeviceAll(user_id)
    deviceList = []
    deviceList2 = []
    deviceDiction = ["deviceSerial", "deviceName", "organization", "addedDate"]
    for device in devices:
        deviceList.append(list(device))
    for dev in deviceList:
        del dev[0]
        deviceList2.append(dict(zip(deviceDiction, dev)))
    item = {
        "data": deviceList2
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=item)


@app.get("/device/{id}", dependencies=[Depends(JWTBearer())], tags=["device"])
async def get_single_device(id: int, Authorization: Optional[str] = Header(None)) -> dict:
    check_db(mydb)
    token = Authorization[7:]
    user_id = jwt.decode(token, JWT_SECRET, algorithms=[
                         JWT_ALGORITHM])["user_id"]
    organization = mydb.getOrganization(user_id)
    device = mydb.getDeviceSingle(id)
    deviceDiction = ["deviceSerial", "deviceName", "organization", "addedDate"]
    try:
        device = list(device)
    except TypeError:
        item = {
            "error": "The device has not registered or not exist"
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=item)
    del device[0]
    if(device[2] == organization):
        item = {
            "data": dict(zip(deviceDiction, device))
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=item)
    elif(device[2] != organization):
        item = {
            "error": "You have no permission to access that device"
        }
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=item)


@ app.delete("/device/{id}", dependencies=[Depends(JWTBearer())], tags=["device"])
async def delete_single_device(id: int, Authorization: Optional[str] = Header(None)) -> dict:
    check_db(mydb)
    token = Authorization[7:]
    user_id = jwt.decode(token, JWT_SECRET, algorithms=[
                         JWT_ALGORITHM])["user_id"]
    organization = mydb.getOrganization(user_id)
    device = mydb.getDeviceSingle(id)
    try:
        device = list(device)
    except TypeError:
        item = {
            "error": "The device has not registered or not exist"
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=item)
    del device[0]
    if(device[2] == organization):
        device = mydb.deleteDeviceSingle(id)
        item = {
            "data": "device deleted"
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=item)
    elif(device[2] != organization):
        item = {
            "error": "You have no permission to access that device"
        }
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=item)
