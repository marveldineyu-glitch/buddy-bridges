import sys; print("V2024-07-24-ANTIDUPLICADOS", flush=True)
import asyncio, re, os, threading, gc, time, urllib.request, hashlib
from collections import deque
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

API_ID = 28074212
API_HASH = "b18dae908474a377684922f3e9d5b795"
CANAL = "@BuddyMovies_canal"
GRUPO = "@BuddyMovies_official"

BRIDGES = [
    {"name": "B1", "token": "8984212389:AAFZMh_ZQZm8DlIqPLvQEljnC1UPVtRJV-Q", "session": "1AZWarzMBuySWi9yMDi6czcZfBDTzaKK3BDAlidU1GSz-nFSaeCpW5SGGb16ga5yYTzCYng9LqSjkL_o2ijHJ69OjJfGcd2i6zM3qcG5O6mG03ommmMXEvJX7HTz0aXtlyR_RCda2SOJf6tq1_GaCdcQBylFdnYcpDl08LZoey8xnZil0afhD1IjFpghUIC1Iha4qoGdZ-D-PFxZfDP2F5tBN0mtouIlxachP4D2jtoprgoqNV53k7HO_WK4opkpQa6EXz0CHGtQsDk1Tj5xwWAL4CVA00YNetysKLCj1rtg4vk5NqY4mx7ZeOcD_2ZmBbS5nMkVc2OvVmprh81ijv4IoN2BaDrU=", "source": "@pooppuuui", "sid": None, "prefix": "/search "},
    {"name": "B2", "token": "8463069047:AAGeZg0IQd-1-Mv3ubxqnwZY1oJgxio9hr8", "session": "1AZWarzMBuySWi9yMDi6czcZfBDTzaKK3BDAlidU1GSz-nFSaeCpW5SGGb16ga5yYTzCYng9LqSjkL_o2ijHJ69OjJfGcd2i6zM3qcG5O6mG03ommmMXEvJX7HTz0aXtlyR_RCda2SOJf6tq1_GaCdcQBylFdnYcpDl08LZoey8xnZil0afhD1IjFpghUIC1Iha4qoGdZ-D-PFxZfDP2F5tBN0mtouIlxachP4D2jtoprgoqNV53k7HO_WK4opkpQa6EXz0CHGtQsDk1Tj5xwWAL4CVA00YNetysKLCj1rtg4vk5NqY4mx7ZeOcD_2ZmBbS5nMkVc2OvVmprh81ijv4IoN2BaDrU=", "source": "@TlgramMovieSearch_Bot", "sid": None, "prefix": ""},
    {"name": "B3", "token": "7690330806:AAFAemkor12n71UAPaoJcnAcnPI_R_Xqygs", "session": "1AZWarzMBuySWi9yMDi6czcZfBDTzaKK3BDAlidU1GSz-nFSaeCpW5SGGb16ga5yYTzCYng9LqSjkL_o2ijHJ69OjJfGcd2i6zM3qcG5O6mG03ommmMXEvJX7HTz0aXtlyR_RCda2SOJf6tq1_GaCdcQBylFdnYcpDl08LZoey8xnZil0afhD1IjFpghUIC1Iha4qoGdZ-D-PFxZfDP2F5tBN0mtouIlxachP4D2jtoprgoqNV53k7HO_WK4opkpQa6EXz0CHGtQsDk1Tj5xwWAL4CVA00YNetysKLCj1rtg4vk5NqY4mx7ZeOcD_2ZmBbS5nMkVc2OvVmprh81ijv4IoN2BaDrU=", "source": "@AutoFilter_Robot", "sid": None, "prefix": ""},
    {"name": "B4", "token": "8808014809:AAEacf05HWO2g4HFWDTlP8IC6lXMBxILqbM", "session": "1AZWarzMBuySWi9yMDi6czcZfBDTzaKK3BDAlidU1GSz-nFSaeCpW5SGGb16ga5yYTzCYng9LqSjkL_o2ijHJ69OjJfGcd2i6zM3qcG5O6mG03ommmMXEvJX7HTz0aXtlyR_RCda2SOJf6tq1_GaCdcQBylFdnYcpDl08LZoey8xnZil0afhD1IjFpghUIC1Iha4qoGdZ-D-PFxZfDP2F5tBN0mtouIlxachP4D2jtoprgoqNV53k7HO_WK4opkpQa6EXz0CHGtQsDk1Tj5xwWAL4CVA00YNetysKLCj1rtg4vk5NqY4mx7ZeOcD_2ZmBbS5nMkVc2OvVmprh81ijv4IoN2BaDrU=", "source": "@Lt_Moviebot", "sid": 8504453537, "prefix": ""},
    {"name": "B5", "token": "8894814453:AAGAuF3cjETqYt_mY2os9raZgMxSZtFqD_E", "session": "1AZWarzMBuySWi9yMDi6czcZfBDTzaKK3BDAlidU1GSz-nFSaeCpW5SGGb16ga5yYTzCYng9LqSjkL_o2ijHJ69OjJfGcd2i6zM3qcG5O6mG03ommmMXEvJX7HTz0aXtlyR_RCda2SOJf6tq1_GaCdcQBylFdnYcpDl08LZoey8xnZil0afhD1IjFpghUIC1Iha4qoGdZ-D-PFxZfDP2F5tBN0mtouIlxachP4D2jtoprgoqNV53k7HO_WK4opkpQa6EXz0CHGtQsDk1Tj5xwWAL4CVA00YNetysKLCj1rtg4vk5NqY4mx7ZeOcD_2ZmBbS5nMkVc2OvVmprh81ijv4IoN2BaDrU=", "source": "@Angela2_moviebot", "sid": 8143714699, "prefix": ""},
    {"name": "B6", "token": "8760379291:AAHHIOGgqTJT0IINcM4dNV2bOYDXHfV0r7I", "session": "1AZWarzMBuySWi9yMDi6czcZfBDTzaKK3BDAlidU1GSz-nFSaeCpW5SGGb16ga5yYTzCYng9LqSjkL_o2ijHJ69OjJfGcd2i6zM3qcG5O6mG03ommmMXEvJX7HTz0aXtlyR_RCda2SOJf6tq1_GaCdcQBylFdnYcpDl08LZoey8xnZil0afhD1IjFpghUIC1Iha4qoGdZ-D-PFxZfDP2F5tBN0mtouIlxachP4D2jtoprgoqNV53k7HO_WK4opkpQa6EXz0CHGtQsDk1Tj5xwWAL4CVA00YNetysKLCj1rtg4vk5NqY4mx7ZeOcD_2ZmBbS5nMkVc2OvVmprh81ijv4IoN2BaDrU=", "source": "@Apple_moviebot", "sid": 8104769075, "prefix": ""},
    {"name": "B7", "token": "8952066629:AAHLnoIl62kY0wf4XrFWKiiDq9UaNbjk9zE", "session": "1AZWarzMBuySWi9yMDi6czcZfBDTzaKK3BDAlidU1GSz-nFSaeCpW5SGGb16ga5yYTzCYng9LqSjkL_o2ijHJ69OjJfGcd2i6zM3qcG5O6mG03ommmMXEvJX7HTz0aXtlyR_RCda2SOJf6tq1_GaCdcQBylFdnYcpDl08LZoey8xnZil0afhD1IjFpghUIC1Iha4qoGdZ-D-PFxZfDP2F5tBN0mtouIlxachP4D2jtoprgoqNV53k7HO_WK4opkpQa6EXz0CHGtQsDk1Tj5xwWAL4CVA00YNetysKLCj1rtg4vk5NqY4mx7ZeOcD_2ZmBbS5nMkVc2OvVmprh81ijv4IoN2BaDrU=", "source": "@gpt3ru_chat_bot", "sid": 6157862059, "prefix": "", "gpt": True}
]

os.environ['PYTHONOPTIMIZE'] = '2'

class Bridge:
    def __init__(self, c):
        self.c = c
        self.last_uid = None
        self.last_name = None
        self.last_rid = None
        self.last_msg_id = None  # Para editar paginación
        self.queue = deque()
        self.bmap = {}
        self.rl = {}
        self.pending = None
        self._sent_ids = set()  # IDs ya procesados para evitar duplicados
        
        h = hashlib.md5(c["token"].encode()).hexdigest()[:8]
        self.bot = TelegramClient(f'b_{c["name"]}_{h}', API_ID, API_HASH, retry_delay=3, auto_reconnect=True, timeout=15)
        self.usr = TelegramClient(StringSession(c["session"]), API_ID, API_HASH, retry_delay=3, auto_reconnect=True, timeout=15)

    def clean(self):
        if len(self._sent_ids) > 100:
            self._sent_ids = set(list(self._sent_ids)[-50:])
        if len(self.bmap) > 5000:
            for k in list(self.bmap.keys())[:2500]: del self.bmap[k]
        gc.collect()

    def ok(self, uid):
        now = time.time()
        if uid in self.rl:
            self.rl[uid] = [t for t in self.rl[uid] if now - t < 60]
            if len(self.rl[uid]) >= 10: return False
        else: self.rl[uid] = []
        self.rl[uid].append(now)
        return True

    def fix(self, txt):
        if not txt: return ""
        txt = re.sub(r'https?://\S+', '', txt)
        txt = re.sub(r'@\w+', '', txt)
        txt = re.sub(r'(?i).*(update|auto.delete|copyright|save.the.file|will.be.deleted|join.|share.bot).*', '', txt)
        txt = re.sub(r'Hey \*\*.*?\*\*!?', '', txt)
        txt = txt.replace('Search Query:', '🔍').replace('Total Results:', '📊').replace('Page:', '📄')
        txt = re.sub(r'\n\s*\n\s*\n', '\n\n', txt)
        return txt.strip()

    def build_btns(self, msg):
        if not msg or not msg.buttons: return None
        out = []
        skip = ['compartir bot', 'añadir a grupo', 'menú principal', 'share bot', 'add to group', 'main menu']
        block = ['terabox', 'LfvtadGw', 'CM_Zone']
        
        for row in msg.buttons:
            r = []
            for btn in row:
                t = (btn.text or '').strip()
                if t.lower() in skip: continue
                
                if btn.url:
                    if any(b in (btn.url or '') for b in block): continue
                    if self.c["name"] == "B5" and 'start=' in btn.url:
                        sd = parse_qs(urlparse(btn.url).query).get('start', [''])[0]
                        if sd:
                            fd = f"s_{sd[:30]}"
                            self.bmap[fd] = (msg.id, msg.buttons.index(row), row.index(btn), sd)
                            r.append(Button.inline(t[:50] or '📥', fd))
                        continue
                    if self.c["name"] in ["B4","B5","B6"]: continue
                    r.append(Button.url(t[:50], btn.url))
                elif btn.data:
                    d = btn.data.decode() if isinstance(btn.data, bytes) else btn.data
                    self.bmap[d] = (msg.id, msg.buttons.index(row), row.index(btn), None)
                    if t in ['\u200b', '\u200b ']:
                        ds = str(btn.data)
                        t = '🌐' if 'lang' in ds else '🎞️' if 'qual' in ds else '▶️' if 'next' in ds or 'nxt' in ds else '📄' if 'pgkb' in ds else '▫️'
                    r.append(Button.inline(t[:50] or '📥', d[:64]))
            if r: out.append(r)
        return out or None

    async def send_or_edit(self, msg, is_edit=False):
        """Envía o edita UN solo mensaje, sin duplicar"""
        if msg.id in self._sent_ids: return
        self._sent_ids.add(msg.id)
        
        txt = msg.text or ''
        
        # GPT
        if self.c.get("gpt"):
            if self.queue and txt:
                _, name, rid = self.queue.popleft()
                await self.bot.send_message(GRUPO, f"🤖 **{name}:**\n\n{self.fix(txt)[:2000]}", reply_to=rid)
            return
        
        if not self.last_uid: return
        
        # Apple archivo pendiente
        if self.c["name"] == "B6" and self.pending and msg.media and not msg.photo:
            puid, pname, prid = self.pending
            self.pending = None
            cap = self.fix(txt) + "\n\n❤️ @BuddyMovies_Bot"
            sent = await self.usr.send_file(CANAL, msg.media, caption=cap)
            link = f"https://t.me/{CANAL[1:]}/{sent.id}"
            await self.bot.send_message(GRUPO, f"🎬 **{pname}**\n\n🔗 {link}", buttons=[[Button.url("🎥 VER CONTENIDO", link)]], reply_to=prid)
            return
        
        # ARCHIVO
        if msg.media:
            raw = self.fix(txt)
            if self.c["name"] in ["B4","B5"]: raw += f"\n\n➠ @BuddyMovies_official\n➠ @BuddyMovies_Bot"
            elif self.c["name"] == "B6": raw += "\n\n❤️ @BuddyMovies_Bot"
            sent = await self.usr.send_file(CANAL, msg.media, caption=raw)
            link = f"https://t.me/{CANAL[1:]}/{sent.id}"
            title = raw.split('\n')[0][:80] if raw else "Archivo"
            await self.bot.send_message(GRUPO, f"🎬 **{self.last_name}**\n📁 {title}\n\n🔗 {link}", buttons=[[Button.url("🎥 VER CONTENIDO", link)]], reply_to=self.last_rid, link_preview=False)
            return
        
        # TEXTO CON BOTONES
        if txt and msg.buttons:
            clean = self.fix(txt)
            if not clean: return
            btns = self.build_btns(msg)
            
            # EDITAR si es paginación
            if is_edit and self.last_msg_id:
                try:
                    await self.bot.edit_message(GRUPO, self.last_msg_id, clean[:4000], buttons=btns)
                    return
                except:
                    pass
            
            # CREAR nuevo
            sent = await self.bot.send_message(GRUPO, clean[:4000], buttons=btns, reply_to=self.last_rid)
            self.last_msg_id = sent.id

    async def on_new(self, event):
        self.clean()
        m = event.message
        sid = self.c.get("sid")
        if sid and m.sender_id != sid: return
        if not sid and (not m.sender or not m.sender.bot): return
        
        txt = m.text or ''
        if any(x in txt.lower() for x in ['buscando','espera','recuerda','ayúdanos','compártelo','gracias','procesando','maldito','comparte','revisa','save the file','will be deleted','select language','please wait']): return
        if re.search(r'no\s+(se\s+encontr|results?|found|available)', txt, re.IGNORECASE): return
        
        await self.send_or_edit(m, is_edit=False)

    async def on_edit(self, event):
        self.clean()
        m = event.message
        sid = self.c.get("sid")
        if sid and m.sender_id != sid: return
        if not sid and (not m.sender or not m.sender.bot or not m.text): return
        
        txt = m.text or ''
        if any(x in txt.lower() for x in ['buscando','espera','procesando','please wait']): return
        if re.search(r'no\s+(se\s+encontr|results?|found|available)', txt, re.IGNORECASE): return
        if not txt or not m.buttons: return
        
        # EDITAR mensaje existente (paginación)
        await self.send_or_edit(m, is_edit=True)

    async def on_msg(self, event):
        self.clean()
        if event.is_private:
            await event.reply("🎬 <b>¡BuddyPelis!</b>\n\n📽️ <b>+5 millones de películas y series</b>\n🔍 Busca sin límites en el grupo\n\n👉 <b>Únete:</b> @BuddyMovies_official", buttons=[[Button.url("🎥 IR AL GRUPO", "https://t.me/BuddyMovies_official")]], link_preview=False)
            return
        if event.out or not event.text: return
        q = event.text.strip()
        if len(q) < 2 or q.startswith("/"): return
        if not self.ok(event.sender_id): return
        
        try: name = (await event.get_sender()).first_name or "Usuario"
        except: name = "Usuario"
        
        self.last_uid = event.sender_id
        self.last_name = name
        self.last_rid = event.message.id
        self.last_msg_id = None  # Reset para nueva búsqueda
        self._sent_ids.clear()   # Limpiar IDs de búsqueda anterior
        
        if self.c.get("gpt"):
            self.queue.append((event.sender_id, name, event.message.id))
        
        await self.usr.send_message(self.c["source"], f"{self.c.get('prefix', '')}{q}")

    async def on_click(self, event):
        data = event.data.decode() if isinstance(event.data, bytes) else event.data
        if not data: return
        
        if data in self.bmap:
            info = self.bmap[data]
            if len(info) > 3 and info[3]:  # start_param
                await event.answer("⚡")
                await self.usr.send_message(self.c["source"], f"/start {info[3]}")
                return
            
            if self.c["name"] == "B6" and self.last_uid:
                self.pending = (self.last_uid, self.last_name, self.last_rid)
            
            try:
                msgs = await self.usr.get_messages(self.c["source"], ids=[info[0]])
                if msgs and msgs[0].buttons:
                    await event.answer("⚡")
                    await msgs[0].buttons[info[1]][info[2]].click()
                    return
            except: pass
        
        # Fallback
        try:
            async for m in self.usr.iter_messages(self.c["source"], limit=50):
                if m.buttons:
                    for ri, row in enumerate(m.buttons):
                        for bi, btn in enumerate(row):
                            bd = btn.data.decode() if isinstance(btn.data, bytes) else btn.data
                            if bd == data:
                                self.bmap[data] = (m.id, ri, bi, None)
                                await event.answer("⚡")
                                await btn.click()
                                return
        except: pass
        
        await event.answer("⏳ Expiró")

    async def start(self):
        await self.usr.start()
        await self.bot.start(bot_token=self.c["token"])
        self.usr.add_event_handler(self.on_new, events.NewMessage(chats=self.c["source"]))
        self.usr.add_event_handler(self.on_edit, events.MessageEdited(chats=self.c["source"]))
        self.bot.add_event_handler(self.on_msg, events.NewMessage)
        self.bot.add_event_handler(self.on_click, events.CallbackQuery)
        print(f"✅ {self.c['name']} listo")
        
        while True:
            await asyncio.sleep(180)
            try: await self.bot.get_me(); await self.usr.get_me(); self.clean()
            except: pass

async def main():
    print(f"🚀 {len(BRIDGES)} bridges")
    await asyncio.gather(*[Bridge(c).start() for c in BRIDGES])

class H(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    def log_message(self, *a): pass

threading.Thread(target=lambda: HTTPServer(("0.0.0.0", int(os.environ.get("PORT",10000))), H).serve_forever(), daemon=True).start()

def ka():
    while True:
        time.sleep(600)
        try: urllib.request.urlopen(f"http://localhost:{int(os.environ.get('PORT',10000))}", timeout=5)
        except: pass
threading.Thread(target=ka, daemon=True).start()

asyncio.run(main())
