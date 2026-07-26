import asyncio
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = 28074212
API_HASH = "b18dae908474a377684922f3e9d5b795"
BOT_TOKEN = "8843453935:AAE3XdnZPOqZSf7Cct7Ei9c2y43d5zZhKwo"
USER_SESSION_STRING = "1AZWarzsBu26nRF7Hs09KajSLH4ccYE0-ikzAFCJMv1ujaF5NeS_0-MdQjp-2uFqM3MH-cD-5cezRnI_HMuQVXIHOOMcQ7MmRLHpGxZRnJdJAyZ5WQl9E3YQMHErmWDjwepv2jiRjdVzTnvaC43ZeONw_ofHcPDUge-ZV3JeURsRcqa8FuC9eTJkQaU0WpFI2lKxFHZxj8E4DQBhbFIKrB3RnvevnZmq9JnOw4hRqfEw2zbbUlenB5Q-L9ljbQbFQy-aW1slvdvBV3CW4QVXI9sBMpf07TIh46QRpn_5oX7WpY7g8mMTW7n9Jkm_lcSkRnADE-7e-A0j4_EVofeUVYnBtkb5yOug="

SOURCE_BOT = "@VoiceShazamBot"
GROUP_ID = "@mabu205"
PORT = int(os.environ.get("PORT", 8080))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        pass

def start_server():
    server = HTTPServer(('0.0.0.0', PORT), HealthHandler)
    logger.info(f"💓 Puerto {PORT}")
    server.serve_forever()

class Bridge:
    def __init__(self):
        self.bot = None
        self.user = None
        self.last_chat = None
        
    async def start(self):
        self.bot = TelegramClient("bot", API_ID, API_HASH)
        await self.bot.start(bot_token=BOT_TOKEN)
        logger.info("✅ Bot OK")
        
        self.user = TelegramClient(StringSession(USER_SESSION_STRING), API_ID, API_HASH)
        await self.user.start()
        logger.info("✅ User OK")
        
        @self.bot.on(events.NewMessage(chats=GROUP_ID))
        async def on_group(event):
            me = await self.bot.get_me()
            if event.sender_id == me.id:
                return
            self.last_chat = event.chat_id
            if event.media:
                await self.user.send_file(SOURCE_BOT, event.media, caption=event.text or "")
            else:
                await self.user.send_message(SOURCE_BOT, event.text or "")
            logger.info("⚡ → VoiceShazamBot")
        
        @self.user.on(events.NewMessage(chats=SOURCE_BOT))
        async def on_source(event):
            if self.last_chat:
                if event.media:
                    await self.bot.send_file(self.last_chat, event.media, caption=event.text or "")
                else:
                    await self.bot.send_message(self.last_chat, event.text or "")
                logger.info("✅ → Grupo")
        
        logger.info("🎉 24/7!")
        await asyncio.gather(
            self.bot.run_until_disconnected(),
            self.user.run_until_disconnected()
        )

if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    asyncio.run(Bridge().start())
