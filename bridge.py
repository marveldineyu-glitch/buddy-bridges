import asyncio, re, os, threading, gc, time, urllib.request
from collections import OrderedDict, deque
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

API_ID = 28074212
API_HASH = "b18dae908474a377684922f3e9d5b795"
CANAL = "@BuddyMovies_canal"
GRUPO = "@BuddyMovies_official"
FOOTER = "\n\n❤️ @BuddyMovies_Bot"

BRIDGES = [
    {"name":"B1","token":"8984212389:AAFZMh_ZQZm8DlIqPLvQEljnC1UPVtRJV-Q","session":"1AZWarzgBu13W0EuNpoxKErbi-sroDDYq6ZWDiIaNcoKjzWrZ5J5uXknAAh-Pq7cgtT-GrhwS5rcoWmzXj5B1EsOIQsFR5qxzoJLAXUPvtEOd8eaV4BsSXyF3G8jRAPqGmbjx7FjepBwg6_TYIDUqeA6CSrkhlSIkNZ-YhTyScCvUoT_0gIQazF4KCC7jsFo1FMxQEPPgJJ3WB0QgRoHqojHEAeJ6MVxcTFmucaQKfjTkrBIlTiQdlHAJzwq7jvOd9c10TUurK0YWPgxfcCE_orEcz_CMhURbK7gJ1kSKHFx-jf3a6MGhzWclKLOkuuizGmOSJnzEkgmfIntIE_Ig3qr2qcbFgno=","source":"@pooppuuui","sid":None,"prefix":"/search "},
    {"name":"B2","token":"8463069047:AAGeZg0IQd-1-Mv3ubxqnwZY1oJgxio9hr8","session":"1AZWarzgBu13W0EuNpoxKErbi-sroDDYq6ZWDiIaNcoKjzWrZ5J5uXknAAh-Pq7cgtT-GrhwS5rcoWmzXj5B1EsOIQsFR5qxzoJLAXUPvtEOd8eaV4BsSXyF3G8jRAPqGmbjx7FjepBwg6_TYIDUqeA6CSrkhlSIkNZ-YhTyScCvUoT_0gIQazF4KCC7jsFo1FMxQEPPgJJ3WB0QgRoHqojHEAeJ6MVxcTFmucaQKfjTkrBIlTiQdlHAJzwq7jvOd9c10TUurK0YWPgxfcCE_orEcz_CMhURbK7gJ1kSKHFx-jf3a6MGhzWclKLOkuuizGmOSJnzEkgmfIntIE_Ig3qr2qcbFgno=","source":"@TlgramMovieSearch_Bot","sid":None,"prefix":""},
    {"name":"B3","token":"7690330806:AAFAemkor12n71UAPaoJcnAcnPI_R_Xqygs","session":"1AZWarzgBu13W0EuNpoxKErbi-sroDDYq6ZWDiIaNcoKjzWrZ5J5uXknAAh-Pq7cgtT-GrhwS5rcoWmzXj5B1EsOIQsFR5qxzoJLAXUPvtEOd8eaV4BsSXyF3G8jRAPqGmbjx7FjepBwg6_TYIDUqeA6CSrkhlSIkNZ-YhTyScCvUoT_0gIQazF4KCC7jsFo1FMxQEPPgJJ3WB0QgRoHqojHEAeJ6MVxcTFmucaQKfjTkrBIlTiQdlHAJzwq7jvOd9c10TUurK0YWPgxfcCE_orEcz_CMhURbK7gJ1kSKHFx-jf3a6MGhzWclKLOkuuizGmOSJnzEkgmfIntIE_Ig3qr2qcbFgno=","source":"@AutoFilter_Robot","sid":None,"prefix":""},
    {"name":"B4","token":"8808014809:AAEacf05HWO2g4HFWDTlP8IC6lXMBxILqbM","session":"1AZWarzgBu13W0EuNpoxKErbi-sroDDYq6ZWDiIaNcoKjzWrZ5J5uXknAAh-Pq7cgtT-GrhwS5rcoWmzXj5B1EsOIQsFR5qxzoJLAXUPvtEOd8eaV4BsSXyF3G8jRAPqGmbjx7FjepBwg6_TYIDUqeA6CSrkhlSIkNZ-YhTyScCvUoT_0gIQazF4KCC7jsFo1FMxQEPPgJJ3WB0QgRoHqojHEAeJ6MVxcTFmucaQKfjTkrBIlTiQdlHAJzwq7jvOd9c10TUurK0YWPgxfcCE_orEcz_CMhURbK7gJ1kSKHFx-jf3a6MGhzWclKLOkuuizGmOSJnzEkgmfIntIE_Ig3qr2qcbFgno=","source":"@Lt_Moviebot","sid":8504453537,"prefix":""},
    {"name":"B5","token":"8894814453:AAGAuF3cjETqYt_mY2os9raZgMxSZtFqD_E","session":"1AZWarzgBu13W0EuNpoxKErbi-sroDDYq6ZWDiIaNcoKjzWrZ5J5uXknAAh-Pq7cgtT-GrhwS5rcoWmzXj5B1EsOIQsFR5qxzoJLAXUPvtEOd8eaV4BsSXyF3G8jRAPqGmbjx7FjepBwg6_TYIDUqeA6CSrkhlSIkNZ-YhTyScCvUoT_0gIQazF4KCC7jsFo1FMxQEPPgJJ3WB0QgRoHqojHEAeJ6MVxcTFmucaQKfjTkrBIlTiQdlHAJzwq7jvOd9c10TUurK0YWPgxfcCE_orEcz_CMhURbK7gJ1kSKHFx-jf3a6MGhzWclKLOkuuizGmOSJnzEkgmfIntIE_Ig3qr2qcbFgno=","source":"@Angela2_moviebot","sid":8143714699,"prefix":""},
    {"name":"B6","token":"8760379291:AAHHIOGgqTJT0IINcM4dNV2bOYDXHfV0r7I","session":"1AZWarzgBu13W0EuNpoxKErbi-sroDDYq6ZWDiIaNcoKjzWrZ5J5uXknAAh-Pq7cgtT-GrhwS5rcoWmzXj5B1EsOIQsFR5qxzoJLAXUPvtEOd8eaV4BsSXyF3G8jRAPqGmbjx7FjepBwg6_TYIDUqeA6CSrkhlSIkNZ-YhTyScCvUoT_0gIQazF4KCC7jsFo1FMxQEPPgJJ3WB0QgRoHqojHEAeJ6MVxcTFmucaQKfjTkrBIlTiQdlHAJzwq7jvOd9c10TUurK0YWPgxfcCE_orEcz_CMhURbK7gJ1kSKHFx-jf3a6MGhzWclKLOkuuizGmOSJnzEkgmfIntIE_Ig3qr2qcbFgno=","source":"@Apple_moviebot","sid":8104769075,"prefix":""},
    {"name":"B7","token":"8952066629:AAHLnoIl62kY0wf4XrFWKiiDq9UaNbjk9zE","session":"1AZWarzgBu13W0EuNpoxKErbi-sroDDYq6ZWDiIaNcoKjzWrZ5J5uXknAAh-Pq7cgtT-GrhwS5rcoWmzXj5B1EsOIQsFR5qxzoJLAXUPvtEOd8eaV4BsSXyF3G8jRAPqGmbjx7FjepBwg6_TYIDUqeA6CSrkhlSIkNZ-YhTyScCvUoT_0gIQazF4KCC7jsFo1FMxQEPPgJJ3WB0QgRoHqojHEAeJ6MVxcTFmucaQKfjTkrBIlTiQdlHAJzwq7jvOd9c10TUurK0YWPgxfcCE_orEcz_CMhURbK7gJ1kSKHFx-jf3a6MGhzWclKLOkuuizGmOSJnzEkgmfIntIE_Ig3qr2qcbFgno=","source":"@gpt3ru_chat_bot","sid":6157862059,"prefix":"","gpt":True}
]

os.environ['PYTHONOPTIMIZE'] = '2'
gc.set_threshold(5000, 50, 50)

# ==================== CLASE BRIDGE (CÓDIGO ORIGINAL UNIFICADO) ====================
class Bridge:
    def __init__(self, c):
        self.c = c
        self.sessions = OrderedDict()
        self.search_results = {}
        self.button_map = {}
        self.msg_map = {}
        self.rl = {}
        self.pending = None
        self.queue = deque()
        self.bot = TelegramClient(f'b_{c["name"]}', API_ID, API_HASH, retry_delay=3, auto_reconnect=True, timeout=15)
        self.usr = TelegramClient(StringSession(c["session"]), API_ID, API_HASH, retry_delay=3, auto_reconnect=True, timeout=15)

    def clean(self):
        now = time.time()
        expired = [k for k, v in self.sessions.items() if now - v.get('t', 0) > 300]
        for k in expired: del self.sessions[k]
        if len(self.search_results) > 100:
            for k in list(self.search_results.keys())[:50]: del self.search_results[k]
        if len(self.button_map) > 2000:
            for k in list(self.button_map.keys())[:1000]: del self.button_map[k]
        gc.collect()

    def ok(self, uid):
        now = time.time()
        if uid in self.rl:
            self.rl[uid] = [t for t in self.rl[uid] if now - t < 60]
            if len(self.rl[uid]) >= 15: return False
        else: self.rl[uid] = []
        self.rl[uid].append(now)
        return True

    def fix(self, txt):
        if not txt: return txt
        txt = txt.replace("@TlgramMovieGroup_Bot", "@BuddyMovies_Bot")
        txt = txt.replace("@FILM_PARADIZE", "@BuddyMovies_official")
        txt = txt.replace("@RZXBOTZ", "@BuddyMovies_Bot")
        txt = re.sub(r'https?://\S+', '', txt)
        txt = re.sub(r'(?i).*(auto.delete|copyright|save.the.file|will.be.deleted|this message|ᴛʜɪs ᴍᴇssᴀɢᴇ).*', '', txt)
        txt = re.sub(r'💭.*', '', txt)
        txt = re.sub(r'♻️.*', '', txt)
        txt = re.sub(r'⚠️.*', '', txt)
        txt = re.sub(r'Hey \*\*.*?\*\*!?', '👋 **¡Hola!**', txt)
        txt = re.sub(r'Search Query:', '🔍 Búsqueda:', txt)
        txt = re.sub(r'Total Results:', '📊 Resultados:', txt)
        txt = re.sub(r'Page:', '📄 Página:', txt)
        return txt.strip()

    def btns(self, msg, our_id=None):
        if not msg or not msg.buttons: return None
        btns = []
        skip = ['compartir bot','añadir a grupo','menú principal','share bot','add to group','main menu']
        block_url = ['LfvtadGw','terabox','d-3RL7TJKnVlN2Nk','CM_Zone','f9RVIwfGDYo2NDM1']
        
        for row in msg.buttons:
            r = []
            for btn in row:
                t = (btn.text or '').strip()
                if t.lower() in skip or 'erotic' in t.lower(): continue
                if btn.url:
                    if any(b in (btn.url or '') for b in block_url): continue
                    if self.c["name"] == "B5" and 'start=' in btn.url:
                        sd = parse_qs(urlparse(btn.url).query).get('start',[''])[0]
                        if sd:
                            fd = f"dl_{sd[:40]}"
                            if our_id: self.button_map[(our_id, fd)] = (msg.id, msg.buttons.index(row), row.index(btn), sd)
                            r.append(Button.inline(t[:50] or '📥', fd))
                        continue
                    if self.c["name"] in ["B4","B5","B6"]: continue
                    r.append(Button.url(t[:50], btn.url))
                elif btn.data:
                    d = btn.data.decode() if isinstance(btn.data, bytes) else btn.data
                    if our_id: self.button_map[(our_id, d)] = (msg.id, msg.buttons.index(row), row.index(btn), None)
                    if t in ['\u200b','\u200b ']:
                        ds = str(btn.data)
                        t = '🌐' if 'lang' in ds else '🎞️' if 'qual' in ds else '▶️' if 'next' in ds or 'nxt' in ds else '📄' if 'pgkb' in ds else '▫️'
                    r.append(Button.inline(t[:50] or '📥', d[:64]))
            if r: btns.append(r)
        return btns or None

    async def on_new(self, event):
        self.clean()
        m = event.message
        sid = self.c.get("sid")
        if sid and m.sender_id != sid: return
        if not sid and (not m.sender or not m.sender.bot): return
        txt = m.text or ''
        block = ['buscando','espera','recuerda usar','ayúdanos','compártelo','gracias','procesando','maldito','comparte','terabox','revisa el anuncio','save the file','will be deleted','select language','please wait']
        if any(x in txt.lower() for x in block): return
        if re.search(r'no\s+(se\s+encontr|results?|found|available)', txt, re.IGNORECASE): return
        
        if self.c.get("gpt"):
            if self.queue and txt:
                _, name, rid = self.queue.popleft()
                await self.bot.send_message(GRUPO, f"🤖 **GPT para {name}:**\n\n{re.sub(r'https?://\S+','',txt).strip()[:2000]}", reply_to=rid)
            return
        
        if not self.sessions: return
        uid = list(self.sessions.keys())[-1]
        s = self.sessions[uid]
        name = s['name']
        
        # Apple pending
        if self.c["name"]=="B6" and self.pending and m.media and not m.photo:
            puid, pname, prid = self.pending
            self.pending = None
            cap = self.fix(txt) + "\n\n❤️ @BuddyMovies_Bot"
            sent = await self.usr.send_file(CANAL, m.media, caption=cap)
            link = f"https://t.me/{CANAL[1:]}/{sent.id}"
            await self.bot.send_message(GRUPO, f"🎬 **{pname}**\n\n🔗 {link}", buttons=[[Button.url("🎥 VER CONTENIDO", link)]], reply_to=prid)
            return
        
        # B6: foto con botones
        if self.c["name"]=="B6" and m.photo and m.buttons:
            path = await m.download_media()
            txt_clean = self.fix(m.text or "Sin descripción")
            b = self.btns(m)
            await self.bot.send_file(GRUPO, path, caption=txt_clean[:1000], buttons=b, reply_to=s['rid'])
            try: os.unlink(path)
            except: pass
            return
        
        # Archivo
        if m.media:
            raw = self.fix(txt) + FOOTER
            sent = await self.usr.send_file(CANAL, m.media, caption=raw)
            link = f"https://t.me/{CANAL[1:]}/{sent.id}"
            title = raw.split('\n')[0][:80] if raw else "Archivo"
            await self.bot.send_message(GRUPO, f"🎬 **{name}**\n📁 {title}\n\n🔗 {link}", buttons=[[Button.url("🎥 VER CONTENIDO", link)]], link_preview=False, reply_to=s['rid'])
            return
        
        # Texto con botones
        if txt and m.buttons and len(txt) > 15:
            clean = self.fix(txt)
            if not clean: return
            
            # EDITAR si ya existe
            if m.id in self.search_results:
                try:
                    b = self.btns(m, self.search_results[m.id][1])
                    await self.bot.edit_message(self.search_results[m.id][0], self.search_results[m.id][1], clean[:4000], buttons=b)
                    return
                except: pass
            
            # CREAR (placeholder + editar)
            sent = await self.bot.send_message(GRUPO, "...", reply_to=s['rid'])
            oid = sent.id
            b = self.btns(m, oid)
            await self.bot.edit_message(GRUPO, oid, clean[:4000], buttons=b)
            self.search_results[m.id] = (GRUPO, oid)

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
        
        clean = self.fix(txt)
        if not clean: return
        
        # EDITAR mensaje existente (paginación)
        if m.id in self.search_results:
            b = self.btns(m, self.search_results[m.id][1])
            try:
                await self.bot.edit_message(self.search_results[m.id][0], self.search_results[m.id][1], clean[:4000], buttons=b)
                return
            except: pass
        
        # Si no está en search_results, enviar nuevo
        if self.sessions:
            uid = list(self.sessions.keys())[-1]
            s = self.sessions[uid]
            sent = await self.bot.send_message(GRUPO, "...", reply_to=s['rid'])
            oid = sent.id
            b = self.btns(m, oid)
            await self.bot.edit_message(GRUPO, oid, clean[:4000], buttons=b)
            self.search_results[m.id] = (GRUPO, oid)

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
        self.sessions[event.sender_id] = {'name': name, 'rid': event.message.id, 't': time.time()}
        self.button_map.clear()
        if self.c.get("gpt"): self.queue.append((event.sender_id, name, event.message.id))
        await self.usr.send_message(self.c["source"], f"{self.c.get('prefix','')}{q}")

    async def on_click(self, event):
        data = event.data.decode() if isinstance(event.data, bytes) else event.data
        if not data: return
        
        # Buscar en button_map por clave (msg_id, data)
        key = (event.message_id, data)
        # También buscar sin msg_id
        info = self.bmap.get(key) or self.bmap.get(data)
        info = None
        if key in self.button_map:
            info = self.button_map[key]
        elif data in self.button_map:
            info = self.button_map[data]
        
        if info:
            if len(info) > 3 and info[3]:
                await event.answer("⚡")
                await self.usr.send_message(self.c["source"], f"/start {info[3]}")
                return
            if self.c["name"]=="B6" and self.sessions:
                uid = list(self.sessions.keys())[-1]
                s = self.sessions[uid]
                self.pending = (uid, s['name'], s['rid'])
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

# ==================== MAIN ====================
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
