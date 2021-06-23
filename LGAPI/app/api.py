from fastapi import FastAPI, Body, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from app.model import UserSchema, UserLoginSchema, DeviceStatusSchema, DeviceSchema
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

microServices = {"user": "http://mmyu.synology.me:10000",
                 "device": "http://mmyu.synology.me:10001", "deviceStatus": "http://mmyu.synology.me:10002"}

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


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    response = RedirectResponse(url=(microServices["user"]+"/user/signup"))
    return response


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    response = RedirectResponse(url=(microServices["user"]+"/user/login"))
    return response


@app.post("/device", dependencies=[Depends(JWTBearer())], tags=["device"])
async def add_device(device: DeviceSchema, Authorization: Optional[str] = Header(None)) -> dict:
    response = RedirectResponse(url=(microServices["device"]+"/device"))
    return response


@app.get("/device", dependencies=[Depends(JWTBearer())], tags=["device"])
async def get_device_list(Authorization: Optional[str] = Header(None)):
    response = RedirectResponse(url=(microServices["device"]+"/device"))
    return response


@app.get("/device/{id}", dependencies=[Depends(JWTBearer())], tags=["device"])
async def get_single_device(id: int, Authorization: Optional[str] = Header(None)) -> dict:
    response = RedirectResponse(url=(microServices["device"]+"/device/{id}"))
    return response


@ app.delete("/device/{id}", dependencies=[Depends(JWTBearer())], tags=["device"])
async def delete_single_device(id: int, Authorization: Optional[str] = Header(None)) -> dict:
    response = RedirectResponse(url=(microServices["device"]+"/device/{id}"))
    return response


@ app.post("/deviceData", tags=["deviceData"])
async def add_data(deviceData: DeviceStatusSchema) -> dict:
    response = RedirectResponse(
        url=(microServices["deviceStatus"]+"/deviceData"))
    return response


@ app.get("/deviceData", dependencies=[Depends(JWTBearer())], tags=["deviceData"])
async def get_deviceData_list(Authorization: Optional[str] = Header(None)):
    response = RedirectResponse(
        url=(microServices["deviceStatus"]+"/deviceData"))
    return response
