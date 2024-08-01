import sys
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Mongo Database
try:
    mongodb = AsyncIOMotorClient(MONGO_URL).ULTRON
except Exception as e:
    logging.error("Failed to connect to MongoDB: %s", e)
    print("Please change your MongoDB settings.")
    sys.exit()

chatsdb = mongodb.tgchatsdb
usersdb = mongodb.tgusersdb

# All Served Users
async def is_served_user(user_id: int) -> bool:
    try:
        user = await usersdb.find_one({"user_id": user_id})
        return bool(user)
    except Exception as e:
        logging.error(f"Error checking if user {user_id} is served: {e}")
        return False

async def get_served_users() -> list:
    users_list = []
    try:
        async for user in usersdb.find({"user_id": {"$gt": 0}}):
            users_list.append(user)
    except Exception as e:
        logging.error(f"Error getting served users: {e}")
    return users_list

async def add_served_user(user_id: int):
    try:
        if not await is_served_user(user_id):
            return await usersdb.insert_one({"user_id": user_id})
    except Exception as e:
        logging.error(f"Error adding served user {user_id}: {e}")

# All Served Chats
async def get_served_chats() -> list:
    chats_list = []
    try:
        async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
            chats_list.append(chat)
    except Exception as e:
        logging.error(f"Error getting served chats: {e}")
    return chats_list

async def is_served_chat(chat_id: int) -> bool:
    try:
        chat = await chatsdb.find_one({"chat_id": chat_id})
        return bool(chat)
    except Exception as e:
        logging.error(f"Error checking if chat {chat_id} is served: {e}")
        return False

async def add_served_chat(chat_id: int):
    try:
        if not await is_served_chat(chat_id):
            return await chatsdb.insert_one({"chat_id": chat_id})
    except Exception as e:
        logging.error(f"Error adding served chat {chat_id}: {e}")
import sys
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Mongo Database
try:
    mongodb = AsyncIOMotorClient(MONGO_URL).ULTRON
except Exception as e:
    logging.error("Failed to connect to MongoDB: %s", e)
    print("Please change your MongoDB settings.")
    sys.exit()

chatsdb = mongodb.tgchatsdb
usersdb = mongodb.tgusersdb

# All Served Users
async def is_served_user(user_id: int) -> bool:
    try:
        user = await usersdb.find_one({"user_id": user_id})
        return bool(user)
    except Exception as e:
        logging.error(f"Error checking if user {user_id} is served: {e}")
        return False

async def get_served_users() -> list:
    users_list = []
    try:
        async for user in usersdb.find({"user_id": {"$gt": 0}}):
            users_list.append(user)
    except Exception as e:
        logging.error(f"Error getting served users: {e}")
    return users_list

async def add_served_user(user_id: int):
    try:
        if not await is_served_user(user_id):
            return await usersdb.insert_one({"user_id": user_id})
    except Exception as e:
        logging.error(f"Error adding served user {user_id}: {e}")

# All Served Chats
async def get_served_chats() -> list:
    chats_list = []
    try:
        async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
            chats_list.append(chat)
    except Exception as e:
        logging.error(f"Error getting served chats: {e}")
    return chats_list

async def is_served_chat(chat_id: int) -> bool:
    try:
        chat = await chatsdb.find_one({"chat_id": chat_id})
        return bool(chat)
    except Exception as e:
        logging.error(f"Error checking if chat {chat_id} is served: {e}")
        return False

async def add_served_chat(chat_id: int):
    try:
        if not await is_served_chat(chat_id):
            return await chatsdb.insert_one({"chat_id": chat_id})
    except Exception as e:
        logging.error(f"Error adding served chat {chat_id}: {e}")
