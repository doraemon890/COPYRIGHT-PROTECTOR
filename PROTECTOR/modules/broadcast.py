import asyncio
import traceback
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.types import Message
from config import OWNER_ID
from PROTECTOR import PROTECTOR as app
from PROTECTOR.helper import get_chats, get_users

async def send_msg(user_id: int, message: Message) -> tuple[int, str]:
    try:
        await message.copy(chat_id=user_id)
        return 200, f"{user_id} : message sent\n"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception:
        return 500, f"{user_id} : {traceback.format_exc()}\n"

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to broadcast it.")
        return

    exmsg = await message.reply_text("Started broadcasting!")

    all_chats = await get_chats() or []
    all_users = await get_users() or []

    print(f"Debug: All Chats - {all_chats}")
    print(f"Debug: All Users - {all_users}")

    done_chats, done_users, failed_chats, failed_users = 0, 0, 0, 0

    for chat in all_chats:
        status, _ = await send_msg(chat, message.reply_to_message)
        if status == 200:
            done_chats += 1
        else:
            failed_chats += 1
        await asyncio.sleep(0.1)

    for user in all_users:
        status, _ = await send_msg(user, message.reply_to_message)
        if status == 200:
            done_users += 1
        else:
            failed_users += 1
        await asyncio.sleep(0.1)

    result_message = f"Successfully broadcasting ✅\n\nSent message to `{done_chats}` chats and `{done_users}` users."
    if failed_chats > 0 or failed_users > 0:
        result_message += f"\n\nNote: Due to some issues, couldn't broadcast to `{failed_users}` users and `{failed_chats}` chats."

    await exmsg.edit_text(result_message)

@app.on_message(filters.command("announce") & filters.user(OWNER_ID))
async def announce(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Reply to some post to broadcast")
        return

    to_send = message.reply_to_message.id
    chats = await get_chats() or []
    users = await get_users() or []

    print(f"Debug: Announce Chats - {chats}")
    print(f"Debug: Announce Users - {users}")

    failed_chats, failed_users = 0, 0

    for chat in chats:
        try:
            await client.forward_messages(chat_id=int(chat), from_chat_id=message.chat.id, message_ids=to_send)
        except Exception:
            failed_chats += 1
        await asyncio.sleep(1)

    for user in users:
        try:
            await client.forward_messages(chat_id=int(user), from_chat_id=message.chat.id, message_ids=to_send)
        except Exception:
            failed_users += 1
        await asyncio.sleep(1)

    await message.reply_text(
        f"Broadcast complete. {failed_chats} groups failed to receive the message, probably due to being kicked. "
        f"{failed_users} users failed to receive the message, probably due to being banned."
    )
