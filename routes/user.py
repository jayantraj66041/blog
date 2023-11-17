from fastapi import APIRouter
from models.user import User
from config.db import conn
from schemas.user import userEntity, usersEntity
from bson import ObjectId

user = APIRouter()


@user.get("/")
async def find_all_users():
    return usersEntity(conn.learning1.user.find())


@user.get("/{id}")
async def find_one_user(id:str):
    return userEntity(conn.learning1.user.find_one({"_id": ObjectId(id)}))

@user.post("/")
async def create_user(user: User):
    conn.learning1.user.insert_one(dict(user))
    return user

@user.put("/{id}")
async def update_user(id:str, user: User):
    conn.learning1.user.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(user)
    })
    return userEntity(conn.learning1.user.find_one({"_id": ObjectId(id)}))

@user.delete("/{id}")
async def delete_user(id:str):
    return userEntity(conn.learning1.user.find_one_and_delete({"_id": ObjectId(id)}))