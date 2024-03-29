from fastapi import APIRouter, WebSocket
from models.user import User
from config.db import conn
from schemas.user import userEntity, usersEntity
from bson import ObjectId


user = APIRouter()


@user.get("/")
async def find_all_users():
    return usersEntity(conn.user.find())


@user.get("/{id}")
async def find_one_user(id:str):
    return userEntity(conn.user.find_one({"_id": ObjectId(id)}))


@user.post("/")
async def create_user(user: User):
    conn.user.insert_one(dict(user))
    return user


@user.put("/{id}")
async def update_user(id:str, user: User):
    conn.user.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(user)
    })
    return userEntity(conn.user.find_one({"_id": ObjectId(id)}))


@user.delete("/{id}")
async def delete_user(id:str):
    return userEntity(conn.user.find_one_and_delete({"_id": ObjectId(id)}))


websocket_list = []
@user.websocket("/ws")
async def counter(websocket: WebSocket):
    await websocket.accept()
    if websocket not in websocket_list:
        websocket_list.append(websocket)

    while True:
        data = await websocket.receive_text()
        if data.lower() == "quit":
            await websocket.send_text("Websocket Closed!!")
            await websocket.close()
            break
        else:
            await websocket.send_text(data)
