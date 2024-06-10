from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_URL)
db_users = mongo.usersdb

async def get_users():
    user_list = []
    async for user in db_users.find({"user": {"$gt": 0}}):
        user_list.append(user['user'])
    print(f"Debug: get_users() -> {user_list}")
    return user_list

async def get_user(user):
    users = await get_users()
    return user in users

async def add_user(user):
    users = await get_users()
    if user not in users:
        await db_users.insert_one({"user": user})

async def del_user(user):
    users = await get_users()
    if user in users:
        await db_users.delete_one({"user": user})
