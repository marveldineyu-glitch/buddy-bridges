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
    {"name": "B1", "token": "8984212389:AAFZMh_ZQZm8DlIqPLvQEljnC1UPVtRJV-Q", "session": "1AZWarzQBu5hWbHakw_V4c82HJA0uCNxvwdS_2JHHEVUbCghWQtCFrCbvfFEAMYTh1sCL3mMpTCJMmETKHXkmgBhynikL_1MTEXJfDlFxjnZQDXf1Glbd5w0HuyCQwEP6K_F2DnAS5vsGtH452l_HDS0uQMAGryhoTV7n5Tr9-5E1DmwY4CfKNV7uzYat15FQ6Nsm_vu8iPnQEwy5w5egiY_xnULhFKIkjWrr9gm7WS_OZbSwmEThy32o3I7zxIO__BiRmAFqPnICFo8OJR_FqU7JYoGvHeScnbgbOGU-bcmFUZrq_sFBbldOn1Y4G0TBw6gLeCCUjhwIh-td7KAjaDIRdaoI_lc=", "source": "@pooppuuui", "sid": None, "prefix": "/search "},
    {"name": "B2", "token": "8463069047:AAGeZg0IQd-1-Mv3ubxqnwZY1oJgxio9hr8", "session": "1AZWarzQBuzncKy_mbzKcjlq0_XeKVuhMaiHWMBs3kkt9hmss9EcHTh9f9RtgQYkoDx4oXfLs8rnlwzNA8AHxmt47X2J3r4YJr0QVNVzX3meQKnDv1EKsnctVofcPlsHGuXPZutTrhs0-rtMFXO8TYMESuLbcu0BlENZDA6LVWzItTe17yMvgWexGLJMIyhO-yIrRxHr4838YkKxdxUflsSkjtSZIV8W4EWtrd6eOcTcZbaQyJEUT6jcyXrePbmfaOjMoOsx1PJF1dQisoPP_C-mRSHgp59Za4LmBM4EqQgzXeoPdUdXFRDkCJAfjzc3p6lnU7HqEtcKmm2EIzY43vj_iKSroOOo=", "source": "@TlgramMovieSearch_Bot", "sid": None, "prefix": ""},
    {"name": "B3", "token": "7690330806:AAFAemkor12n71UAPaoJcnAcnPI_R_Xqygs", "session": "1AZWarzQBu2q3JnP8YtBiwtloyr8QVF6AOFug129qO5bNQIRLsvnGelrXXIRdVYezjgm0IJNH5d_3lIBSNTxBTQnSss_Oz_MQksUSw1883Vbx5O3RyUM6UhYxhPe9jNuCHFhfTPn3iwxlQ63tJiNJ_Dd7ndNYdDFKsnrnKDvOkGX6H6UZyABCKj25nq8MCp6LRs22lV-AkmmVkdPRwL2CF7bIosmIHnfOrA2VxO_8ozC-iB08xA19YEqQtbA6YxCcYVgQuJAAyqqRIhqtHSibUloyqzYiLGUX7wWKPjYOrGOI4X-_NJAmTlkIvtQQHwd1HKI6NVLjnLker7Nas0wwUja1lOCfpQI=", "source": "@AutoFilter_Robot", "sid": None, "prefix": ""},
    {"name": "B4", "token": "8808014809:AAEacf05HWO2g4HFWDTlP8IC6lXMBxILqbM", "session": "1AZWarzQBuw2Qy79iGpD5cWK5pf1LtqHo8f-gjYTl7G8c4wcEvAXuhRifBWgMyrQeXsW62Jpv2YbE3yQJJC1D520D4CPbkOHM5c9NUlDOaQNGDg4gbTzf00Ye6KlbLifZpgQI9Zk3SO9EeMJlq7MVvqUNUgMpCaxYl3oMcAhhqnzHPgMmdQR9epRSKMU6d_PeQ7NHThlpYHHYB5wpMBz2-IaajdMMXPB4-shgmIHGeh_BdQy6UArhkcLFaxCu-f60MK39MUzYq4UElN0aaSn7HuSfaszh5QlALJQe9AZrP1Jsa7UzErtsZ0JDsoMt6ujcvgpXCYu3xYQkNTQh1s7n-qb4y8uaQZU=", "source": "@Lt_Moviebot", "sid": 8504453537, "prefix": ""},
    {"name": "B5", "token": "8894814453:AAGAuF3cjETqYt_mY2os9raZgMxSZtFqD_E", "session": "1AZWarzQBuw2Qy79iGpD5cWK5pf1LtqHo8f-gjYTl7G8c4wcEvAXuhRifBWgMyrQeXsW62Jpv2YbE3yQJJC1D520D4CPbkOHM5c9NUlDOaQNGDg4gbTzf00Ye6KlbLifZpgQI9Zk3SO9EeMJlq7MVvqUNUgMpCaxYl3oMcAhhqnzHPgMmdQR9epRSKMU6d_PeQ7NHThlpYHHYB5wpMBz2-IaajdMMXPB4-shgmIHGeh_BdQy6UArhkcLFaxCu-f60MK39MUzYq4UElN0aaSn7HuSfaszh5QlALJQe9AZrP1Jsa7UzErtsZ0JDsoMt6ujcvgpXCYu3xYQkNTQh1s7n-qb4y8uaQZU=", "source": "@Angela2_moviebot", "sid": 8143714699, "prefix": ""},
    {"name": "B6", "token": "8760379291:AAHHIOGgqTJT0IINcM4dNV2bOYDXHfV0r7I", "session": "1AZWarzQBu3ZUy3OFCmSneDqRGmhmOequJNsxnU2U1n1U5gCumQo2B_7ve5en_f8KEmXMp7WUE-nWX3SnvxNuBG4xItjnz6L4rYVbZ-OhxEFX8WrF4PdGNXgWWqkgxlH9O7NEZfspmsiRd9QTE9WO0ZRhl-UcY9zXh_066TUxbsInY71vL-0GZjvHHGn1afy9Gj7nphO5h8ockeypg9Kx5bYOJ1bRki36iyrVNbUTpMfFiB4KkEAC1hFlqYoo56EEVEy7piw0TR2L3QDCZnahy3XI8Azpt0JPIc0Y5TZCDUcYyWQtkS5H_CKvnxVTIPitWadXZVHIrQRXz3Lj2KvF6ZyiYUESy0g=", "source": "@Apple_moviebot", "sid": 8104769075, "prefix": ""},
    {"name": "B7", "token": "8952066629:AAHLnoIl62kY0wf4XrFWKiiDq9UaNbjk9zE", "session": "1AZWarzsBu3ny9-HTgWpuIkTxb2vRDvQJu0tU-l_79zEFPRsg1fX4vV7aQw5Qew3KyFIi7-VuZDR3niQvGaXRh89KP2AywppMfdolEwgquZIRROPPNuLQovcl5hpp4vvt6r1gb6Zr1EZrOBOp4PKiG2RLff0b2bKWzRPd-pr5CbDPtTrIBSFMXnMCDwZvs8wxB6n1KZ6H6b5Ndunvr3yOhSKDfzqhWq8Rz3HpGq6iWo1vI418VFHbUXVvlGBe47jEDQc6eaosxAv1EFjRVbmumdQT7aF1GW3u-H_pfpRwpYQHb0r3hVBMCva6eDuTZ_L5rOaE2Zix41Z3C51umX6FZjdHGuyed20=", "source": "@gpt3ru_chat_bot", "sid": 6157862059, "prefix": "", "gpt": True}
]

os.environ['PYTHONOPTIMIZE'] = '2'

class Bridge:
    def __init__(self, c):
        self.c = c
        self.last = {}  # uid -> {name, rid, msg_id}
        self.queue = deque()
        self.bmap = {}  # (chat, msg, data) -> (orig_msg, row, col, start)
        self.rl = {}
        self.pending = None
        self.lock = asyncio.Lock()
        
        h = hashlib.md5(c["token"].encode()).hexdigest()[:8]
        self.bot = TelegramClient(f'b_{c["name"]}_{h}', API_ID, API_HASH, retry_delay=3, auto_reconnect=True, timeout=15)
        self.usr = TelegramClient(StringSession(c["session"]), API_ID, API_HASH, retry_delay=3, auto_reconnect=True, timeout=15)

    def clean(self):
        now = time.time()
        for k in list(self.last.keys()):
            if now - self.last[k].get('t', 0) > 300: del self.last[k]
        if len(self.bmap) > 5000:
            for k in list(self.bmap.keys())[:2500]: del self.bmap[k]
        if self.c.get("gpt") and len(self.queue) > 50:
            for _ in range(25): self.queue.popleft()
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

    async def handle_msg(self, m, uid):
        """Procesa UN mensaje - sin duplicados"""
        txt = m.text or ''
        
        # GPT
        if self.c.get("gpt"):
            if self.queue and txt:
                _, name, rid = self.queue.popleft()
                await self.bot.send_message(GRUPO, f"🤖 **{name}:**\n\n{self.fix(txt)[:2000]}", reply_to=rid)
            return
        
        if uid not in self.last: return
        name = self.last[uid]['name']
        rid = self.last[uid]['rid']
        
        # Apple archivo pendiente
        if self.c["name"] == "B6" and self.pending and m.media and not m.photo:
            puid, pname, prid = self.pending
            self.pending = None
            cap = self.fix(txt) + "\n\n❤️ @BuddyMovies_Bot"
            sent = await self.usr.send_file(CANAL, m.media, caption=cap)
            link = f"https://t.me/{CANAL[1:]}/{sent.id}"
            await self.bot.send_message(GRUPO, f"🎬 **{pname}**\n\n🔗 {link}", buttons=[[Button.url("🎥 VER CONTENIDO", link)]], reply_to=prid)
            return
        
        # ARCHIVO -> siempre al canal y luego link al grupo
        if m.media:
            raw = self.fix(txt)
            if self.c["name"] in ["B4","B5"]: raw += f"\n\n➠ @BuddyMovies_official\n➠ @BuddyMovies_Bot"
            elif self.c["name"] == "B6": raw += "\n\n❤️ @BuddyMovies_Bot"
            sent = await self.usr.send_file(CANAL, m.media, caption=raw)
            link = f"https://t.me/{CANAL[1:]}/{sent.id}"
            title = raw.split('\n')[0][:80] if raw else "Archivo"
            await self.bot.send_message(GRUPO, f"🎬 **{name}**\n📁 {title}\n\n🔗 {link}", buttons=[[Button.url("🎥 VER CONTENIDO", link)]], reply_to=rid, link_preview=False)
            return
        
        # TEXTO CON BOTONES -> editar si ya existe, si no crear
        if txt and m.buttons and len(txt) > 15:
            clean = self.fix(txt)
            if not clean: return
            btns = self.build_btns(m)
            
            # Si ya hay un mensaje previo de esta búsqueda, EDITAR
            if 'msg_id' in self.last[uid]:
                try:
                    await self.bot.edit_message(GRUPO, self.last[uid]['msg_id'], clean[:4000], buttons=btns)
                    # Actualizar bmap para el mensaje editado
                    self.update_bmap(m, GRUPO, self.last[uid]['msg_id'])
                    return
                except:
                    pass
            
            # Si no, crear nuevo
            sent = await self.bot.send_message(GRUPO, clean[:4000], buttons=btns, reply_to=rid)
            self.last[uid]['msg_id'] = sent.id
            self.update_bmap(m, sent.chat_id, sent.id)

    def build_btns(self, msg):
        """Construye botones con datos inline para paginación"""
        if not msg or not msg.buttons: return None
        out = []
        block = ['terabox', 'LfvtadGw', 'CM_Zone']
        skip = ['compartir bot', 'añadir a grupo', 'menú principal', 'share bot', 'add to group', 'main menu']
        
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
                            r.append(Button.inline(t[:50] or '📥', fd))
                        continue
                    if self.c["name"] in ["B4","B5","B6"]: continue
                    r.append(Button.url(t[:50], btn.url))
                elif btn.data:
                    d = btn.data.decode() if isinstance(btn.data, bytes) else btn.data
                    if t in ['\u200b', '\u200b ']:
                        ds = str(btn.data)
                        t = '🌐' if 'lang' in ds else '🎞️' if 'qual' in ds else '▶️' if 'next' in ds or 'nxt' in ds else '📄' if 'pgkb' in ds else '▫️'
                    r.append(Button.inline(t[:50] or '📥', d[:64]))
            if r: out.append(r)
        return out or None

    def update_bmap(self, msg, chat, mid):
        """Guarda referencias de botones para clicks"""
        if not msg or not msg.buttons: return
        for ri, row in enumerate(msg.buttons):
            for bi, btn in enumerate(row):
                if btn.data:
                    d = btn.data.decode() if isinstance(btn.data, bytes) else btn.data
                    self.bmap[(chat, mid, d)] = (msg.id, ri, bi, None)
                elif btn.url and self.c["name"] == "B5" and 'start=' in btn.url:
                    sd = parse_qs(urlparse(btn.url).query).get('start', [''])[0]
                    if sd:
                        fd = f"s_{sd[:30]}"
                        self.bmap[(chat, mid, fd)] = (msg.id, ri, bi, sd)

    async def on_new(self, event):
        self.clean()
        m = event.message
        sid = self.c.get("sid")
        if sid and m.sender_id != sid: return
        if not sid and (not m.sender or not m.sender.bot): return
        
        txt = m.text or ''
        if any(x in txt.lower() for x in ['buscando','espera','recuerda','ayúdanos','compártelo','gracias','procesando','maldito','comparte','revisa','save the file','will be deleted','select language','please wait']): return
        if re.search(r'no\s+(se\s+encontr|results?|found|available)', txt, re.IGNORECASE): return
        
        # Buscar el último usuario que hizo búsqueda
        if self.last:
            uid = list(self.last.keys())[-1]
            await self.handle_msg(m, uid)

    async def on_edit(self, event):
        """EDIT del bot fuente -> editar en grupo también"""
        self.clean()
        m = event.message
        sid = self.c.get("sid")
        if sid and m.sender_id != sid: return
        if not sid and (not m.sender or not m.sender.bot): return
        
        txt = m.text or ''
        if any(x in txt.lower() for x in ['buscando','espera','procesando','please wait']): return
        if re.search(r'no\s+(se\s+encontr|results?|found|available)', txt, re.IGNORECASE): return
        if not txt or not m.buttons: return
        
        # Buscar último usuario
        if not self.last: return
        uid = list(self.last.keys())[-1]
        
        clean = self.fix(txt)
        if not clean: return
        btns = self.build_btns(m)
        
        # Si hay mensaje previo, EDITAR (paginación)
        if uid in self.last and 'msg_id' in self.last[uid]:
            try:
                await self.bot.edit_message(GRUPO, self.last[uid]['msg_id'], clean[:4000], buttons=btns)
                self.update_bmap(m, GRUPO, self.last[uid]['msg_id'])
                return
            except:
                pass
        
        # Si no, crear nuevo
        if uid in self.last:
            sent = await self.bot.send_message(GRUPO, clean[:4000], buttons=btns, reply_to=self.last[uid]['rid'])
            self.last[uid]['msg_id'] = sent.id
            self.update_bmap(m, sent.chat_id, sent.id)

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
        
        self.last[event.sender_id] = {'name': name, 'rid': event.message.id, 't': time.time()}
        
        if self.c.get("gpt"):
            self.queue.append((event.sender_id, name, event.message.id))
        
        await self.usr.send_message(self.c["source"], f"{self.c.get('prefix', '')}{q}")

    async def on_click(self, event):
        data = event.data.decode() if isinstance(event.data, bytes) else event.data
        if not data: return
        
        key = (event.chat_id, event.message_id, data)
        
        # Buscar en caché
        if key in self.bmap:
            info = self.bmap[key]
            if len(info) > 3 and info[3]:  # start_param
                await event.answer("⚡")
                await self.usr.send_message(self.c["source"], f"/start {info[3]}")
                return
            
            if self.c["name"] == "B6":
                for uid, v in self.last.items():
                    self.pending = (uid, v['name'], v['rid'])
                    break
            
            try:
                msgs = await self.usr.get_messages(self.c["source"], ids=[info[0]])
                if msgs and msgs[0].buttons:
                    await event.answer("⚡")
                    await msgs[0].buttons[info[1]][info[2]].click()
                    return
            except: pass
        
        # Fallback: buscar en mensajes recientes
        try:
            async for m in self.usr.iter_messages(self.c["source"], limit=50):
                if m.buttons:
                    for ri, row in enumerate(m.buttons):
                        for bi, btn in enumerate(row):
                            bd = btn.data.decode() if isinstance(btn.data, bytes) else btn.data
                            if bd == data:
                                self.bmap[(event.chat_id, event.message_id, data)] = (m.id, ri, bi, None)
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
