import asyncio
import importlib
from pyrogram import idle
from PROTECTOR import PROTECTOR
from PROTECTOR.modules import ALL_MODULES

LOGGER_ID = -1002059718978

loop = asyncio.get_event_loop()

async def JARVIS():
    for all_module in ALL_MODULES:
        try:
            importlib.import_module("PROTECTOR.modules." + all_module)
        except Exception as e:
            print(f"Failed to import module {all_module}: {e}")
    print("Bot Started Successfully")
    
    try:
        await PROTECTOR.send_message(LOGGER_ID, "**𝖨 𝖺𝗆 𝖺𝗅𝗂𝗏𝖾 𝖡𝖺𝖻𝗒 𝖸𝗈𝗎𝗋 𝖡𝗈𝗍 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅 𝖣𝖾𝗉𝗅𝗈𝗒 \n Mʏ Dᴇᴠᴇʟᴏᴘᴇʀ  [JARVIS](https://t.me/JARVIS_V2)**")
    except Exception as e:
        print(f"Failed to send message to LOGGER_ID: {e}")
    
    await idle()

if __name__ == "__main__":
    loop.run_until_complete(JARVIS())
