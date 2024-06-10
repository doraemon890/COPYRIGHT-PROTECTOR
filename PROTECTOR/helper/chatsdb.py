from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_URL)
db = mongo.get_database("Kishu")  # Ensure this points to the correct database name
chats_collection = db.get_collection("chatsdb")  # Ensure this points to the correct collection name

async def get_chats():
    chat_list = []
    async for chat in chats_collection.find({"chat": {"$lt": 0}}):
        chat_list.append(chat['chat'])
    print(f"Debug: get_chats() -> {chat_list}")
    return chat_list

async def get_chat(chat):
    chats = await get_chats()
    return chat in chats

async def add_chat(chat):
    chats = await get_chats()
    if chat not in chats:
        await chats_collection.insert_one({"chat": chat})

async def del_chat(chat):
    chats = await get_chats()
    if chat in chats:
        await chats_collection.delete_one({"chat": chat})
