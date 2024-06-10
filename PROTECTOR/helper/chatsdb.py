from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_URL)
db_chats = mongo.chatsdb

async def get_chats():
    chat_list = []
    async for chat in db_chats.find({"chat": {"$lt": 0}}):
        chat_list.append(chat['chat'])
    print(f"Debug: get_chats() -> {chat_list}")
    return chat_list

async def get_chat(chat):
    chats = await get_chats()
    return chat in chats

async def add_chat(chat):
    chats = await get_chats()
    if chat not in chats:
        await db_chats.insert_one({"chat": chat})

async def del_chat(chat):
    chats = await get_chats()
    if chat in chats:
        await db_chats.delete_one({"chat": chat})
