import asyncio
import importlib
from pyrogram import idle
from PROTECTOR import PROTECTOR
from PROTECTOR.modules import ALL_MODULES

LOGGER_ID = -1002014167331

loop = asyncio.get_event_loop()

async def JARVIS():
    for all_module in ALL_MODULES:
        importlib.import_module("PROTECTOR.modules." + all_module)
    print("Bot Started Successfully")
    await idle()
    print("MAI HU PIRO CODER BOLO NHI AAYA ERROR")
    await PROTECTOR.send_message(LOGGER_ID, "**ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ ʏᴏᴜʀ ʙᴏᴛ ᴅᴇᴘʟᴏʏᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ✅ \n ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ  [JARVIS](https://t.me/JARVIS_V2)**")

if __name__ == "__main__":
    loop.run_until_complete(JARVIS())
    
