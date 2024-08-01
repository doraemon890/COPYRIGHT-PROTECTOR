from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_USERNAME = getenv("BOT_USERNAME")
OWNER_ID = int(getenv("OWNER_ID"))
LOGGER_ID = int(getenv("LOGGER_ID"))
MONGO_URL = getenv("MONGO_URL")

SUDOERS = filters.user([7044783841])