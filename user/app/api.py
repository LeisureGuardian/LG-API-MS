from fastapi import FastAPI, Body, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.model import UserSchema, UserLoginSchema
from app.auth.auth_handler import signJWT
from app.db import DB
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


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    check_db(mydb)
    try:
        mydb.addUser(user)
    except pymysql.err.IntegrityError:
        item = {
            "error": "Duplicate email"
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=item)
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    check_db(mydb)
    if check_user(user):
        return signJWT(user.email)
    item = {
        "error": "Login Failed"
    }
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=item)
