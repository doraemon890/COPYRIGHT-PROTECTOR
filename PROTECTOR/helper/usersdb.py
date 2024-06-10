from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_URL)
db = mongo.get_database("Kishu")  # Ensure this points to the correct database name
users_collection = db.get_collection("usersdb")  # Ensure this points to the correct collection name

async def get_users():
    user_list = []
    async for user in users_collection.find({"user": {"$gt": 0}}):
        user_list.append(user['user'])
    print(f"Debug: get_users() -> {user_list}")
    return user_list

async def get_user(user):
    users = await get_users()
    return user in users

async def add_user(user):
    users = await get_users()
    if user not in users:
        await users_collection.insert_one({"user": user})

async def del_user(user):
    users = await get_users()
    if user in users:
        await users_collection.delete_one({"user": user})
