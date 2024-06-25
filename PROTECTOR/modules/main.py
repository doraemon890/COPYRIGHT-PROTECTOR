import logging
import os
import platform
import psutil
import time
import json

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import BOT_USERNAME, OWNER_ID
from PROTECTOR import PROTECTOR as app
from config import *

# Constants
START_TEXT = """<b>🤖 ᴄᴏᴘʏʀɪɢʜᴛ ᴘʀᴏᴛᴇᴄᴛᴏʀ 🛡️</b>

ʜᴇʏ ᴛʜɪs ɪs ᴄᴏᴘʏʀɪɢʜᴛ ᴘʀᴏᴛᴇᴄᴛᴏʀ ʀᴏʙᴏᴛ 🤖\n
ᴡᴇ ᴇɴsᴜʀᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ's sᴇᴄᴜʀɪᴛʏ 📌\n
ᴛʜɪs ʙᴏᴛ ᴄᴀɴ ʀᴇᴍᴏᴠᴇ ʟᴏɴɢ ᴇᴅɪᴛᴇᴅ ᴛᴇxᴛs ᴀɴᴅ ᴄᴏᴘʏʀɪɢʜᴛᴇᴅ ᴍᴀᴛᴇʀɪᴀʟ 📁\n
ᴊᴜsᴛ ᴀᴅᴅ ᴛʜɪs ʙᴏᴛ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ɪᴛ ᴀɴ ᴀᴅᴍɪɴ\n
ғᴇᴇʟ ғʀᴇᴇ ғʀᴏᴍ ᴀɴʏ ᴛʏᴘᴇ ᴏғ **ᴄᴏᴘʏʀɪɢʜᴛ** 🛡️
"""
AUTHORIZED_USERS_FILE = "authorized_users.json"
MAX_MESSAGE_LENGTH = 40

# Load authorized users from file
def load_authorized_users():
    if os.path.exists(AUTHORIZED_USERS_FILE):
        with open(AUTHORIZED_USERS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save authorized users to file
def save_authorized_users(users):
    with open(AUTHORIZED_USERS_FILE, "w") as f:
        json.dump(users, f)

AUTHORIZED_USERS = load_authorized_users()

# Utility functions
def time_formatter(milliseconds: float) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

def size_formatter(bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            break
        bytes /= 1024.0
    return f"{bytes:.2f} {unit}"

# Command Handlers
@app.on_message(filters.command("start"))
async def start_command_handler(_, msg):
    buttons = [
        [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("• ʜᴀɴᴅʟᴇʀ •", callback_data="vip_back")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await msg.reply_photo(
        photo="https://telegra.ph/file/8f6b2cc26b522a252b16a.jpg",
        caption=START_TEXT,
        reply_markup=reply_markup
    )

@app.on_message(filters.command("ping"))
async def activevc(_, message: Message):
    uptime = time_formatter((time.time() - start_time) * 1000)
    cpu = psutil.cpu_percent()
    storage = psutil.disk_usage('/')
    python_version = platform.python_version()

    reply_text = (
        f"➪ᴜᴘᴛɪᴍᴇ: {uptime}\n"
        f"➪ᴄᴘᴜ: {cpu}%\n"
        f"➪ꜱᴛᴏʀᴀɢᴇ: {size_formatter(storage.total)} [ᴛᴏᴛᴀʟ]\n"
        f"➪{size_formatter(storage.used)} [ᴜsᴇᴅ]\n"
        f"➪{size_formatter(storage.free)} [ғʀᴇᴇ]\n"
        f"➪ᴊᴀʀᴠɪs ᴠᴇʀsɪᴏɴ: {python_version}"
    )
    await message.reply(reply_text, quote=True)

@app.on_message(filters.command("auth") & filters.group)
async def auth_user(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    member = await app.get_chat_member(chat_id, user_id)
    if member.status != 'creator':
        await message.reply_text("You must be the group owner to authorize users.")
        return

    if len(message.command) != 2:
        await message.reply_text("Usage: /auth <user_id>")
        return

    auth_user_id = int(message.command[1])
    if chat_id not in AUTHORIZED_USERS:
        AUTHORIZED_USERS[chat_id] = []

    if auth_user_id not in AUTHORIZED_USERS[chat_id]:
        AUTHORIZED_USERS[chat_id].append(auth_user_id)
        save_authorized_users(AUTHORIZED_USERS)
        await message.reply_text(f"User {auth_user_id} has been authorized for this group.")
    else:
        await message.reply_text(f"User {auth_user_id} is already authorized for this group.")

@app.on_message(filters.command("unauth") & filters.group)
async def unauth_user(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    member = await app.get_chat_member(chat_id, user_id)
    if member.status != 'creator':
        await message.reply_text("You must be the group owner to unauthorize users.")
        return

    if len(message.command) != 2:
        await message.reply_text("Usage: /unauth <user_id>")
        return

    unauth_user_id = int(message.command[1])
    if chat_id in AUTHORIZED_USERS and unauth_user_id in AUTHORIZED_USERS[chat_id]:
        AUTHORIZED_USERS[chat_id].remove(unauth_user_id)
        save_authorized_users(AUTHORIZED_USERS)
        await message.reply_text(f"User {unauth_user_id} has been unauthorized for this group.")
    else:
        await message.reply_text(f"User {unauth_user_id} is not authorized for this group.")

@app.on_message(filters.command("listauth") & filters.group)
async def list_authorized_users(_, message: Message):
    chat_id = message.chat.id

    if chat_id not in AUTHORIZED_USERS or not AUTHORIZED_USERS[chat_id]:
        await message.reply_text("No users are currently authorized for this group.")
        return

    authorized_users = "\n".join(map(str, AUTHORIZED_USERS[chat_id]))
    await message.reply_text(f"Authorized users for this group:\n{authorized_users}")

# Callback Query Handlers
@app.on_callback_query(filters.regex("vip_back"))
async def vip_back_callback_handler(_, query: CallbackQuery):
    await query.message.edit_caption(caption=START_TEXT, reply_markup=InlineKeyboardMarkup(gd_buttons))

@app.on_callback_query(filters.regex("back_to_start"))
async def back_to_start_callback_handler(_, query: CallbackQuery):
    await query.answer()
    await query.message.delete()
    await start_command_handler(_, query.message)

# Message Handlers
async def delete_long_edited_messages(client, edited_message: Message):
    chat_id = edited_message.chat.id
    if edited_message.from_user.id in AUTHORIZED_USERS.get(chat_id, []) or (await app.get_chat_member(chat_id, edited_message.from_user.id)).status == 'creator':
        return
    if edited_message.text and len(edited_message.text.split()) > 15:
        await edited_message.reply_text(f"{edited_message.from_user.mention}, ʏᴏᴜʀ ᴇᴅɪᴛᴇᴅ ᴍᴇssᴀɢᴇ ɪs ᴛᴏᴏ ʟᴏɴɢ ᴛʜᴀᴛ's ᴡʜʏ ɪ ʜᴀᴠᴇ ᴅᴇʟᴇᴛᴇᴅ ɪᴛ.")
        await edited_message.delete()
    elif edited_message.sticker or edited_message.animation or edited_message.emoji:
        return

@app.on_edited_message(filters.group & ~filters.me)
async def handle_edited_messages(_, edited_message: Message):
    await delete_long_edited_messages(_, edited_message)

async def delete_long_messages(client, message: Message):
    chat_id = message.chat.id
    if message.from_user.id in AUTHORIZED_USERS.get(chat_id, []) or (await app.get_chat_member(chat_id, message.from_user.id)).status == 'creator':
        return
    if message.text and len(message.text.split()) > MAX_MESSAGE_LENGTH:
        await message.reply_text(f"{message.from_user.mention}, ᴘʟᴇᴀsᴇ ᴋᴇᴇᴘ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ sʜᴏʀᴛ.")
        await message.delete()

@app.on_message(filters.group & ~filters.me)
async def handle_messages(_, message: Message):
    await delete_long_messages(_, message)
