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

BRIDGES = [
    {
        "name": "BuddyMovies",
        "token": "8984212389:AAFZMh_ZQZm8DlIqPLvQEljnC1UPVtRJV-Q",
        "session": "1AZWarzgBu7jej2sCVzECGYhhyLC6ZPpyuIhEVSVXQ7QvYEH1_VpohEG5trvsjNiKBwpEYT1EK2oatfxVmR0WlGrQmvzEsl-uEhbLNmxP7mmEMtxcxLbICa4IYJZdjugBdyyJw89zGH_hqBE3vwCcoEH76R-Mc1TK6ODGhgJMBUqvn-b95kkujG1CcvZhv3ddjR8_Hd_ZVNaJBCyUtTQMTqGGfFYgXzymuoFrTEF8Vsinl9-OfukCbnO3dLMS4AtmZ72qo51SnTk144LLrtVzBTndd5I8XcQ2ab8zGQdNhMXVCFsR4ddwAXI2JfFWA2iUw7KjnROJ7k9EiQR1zZiKKt3s6-d4WV4=",
        "source": "@pooppuuui",
        "source_id": 7537528826,
        "prefix": "/search ",
        "block": ["buscando", "espera", "recuerda usar", "ayúdanos", "compártelo", "gracias"]
    },
    {
        "name": "BuddyNotify",
        "token": "8463069047:AAGeZg0IQd-1-Mv3ubxqnwZY1oJgxio9hr8",
        "session": "1AZWarzgBu7jej2sCVzECGYhhyLC6ZPpyuIhEVSVXQ7QvYEH1_VpohEG5trvsjNiKBwpEYT1EK2oatfxVmR0WlGrQmvzEsl-uEhbLNmxP7mmEMtxcxLbICa4IYJZdjugBdyyJw89zGH_hqBE3vwCcoEH76R-Mc1TK6ODGhgJMBUqvn-b95kkujG1CcvZhv3ddjR8_Hd_ZVNaJBCyUtTQMTqGGfFYgXzymuoFrTEF8Vsinl9-OfukCbnO3dLMS4AtmZ72qo51SnTk144LLrtVzBTndd5I8XcQ2ab8zGQdNhMXVCFsR4ddwAXI2JfFWA2iUw7KjnROJ7k9EiQR1zZiKKt3s6-d4WV4=",
        "source": "@TlgramMovieSearch_Bot",
        "source_id": None,
        "prefix": "",
        "block": ["procesando", "espera", "maldito", "comparte", "terabox", "revisa el anuncio"],
        "skip_btn": ["compartir bot", "añadir a grupo", "menú principal"]
    },
    {
        "name": "AutoFilter",
        "token": "7690330806:AAFAemkor12n71UAPaoJcnAcnPI_R_Xqygs",
        "session": "1AZWarzgBu7jej2sCVzECGYhhyLC6ZPpyuIhEVSVXQ7QvYEH1_VpohEG5trvsjNiKBwpEYT1EK2oatfxVmR0WlGrQmvzEsl-uEhbLNmxP7mmEMtxcxLbICa4IYJZdjugBdyyJw89zGH_hqBE3vwCcoEH76R-Mc1TK6ODGhgJMBUqvn-b95kkujG1CcvZhv3ddjR8_Hd_ZVNaJBCyUtTQMTqGGfFYgXzymuoFrTEF8Vsinl9-OfukCbnO3dLMS4AtmZ72qo51SnTk144LLrtVzBTndd5I8XcQ2ab8zGQdNhMXVCFsR4ddwAXI2JfFWA2iUw7KjnROJ7k9EiQR1zZiKKt3s6-d4WV4=",
        "source": "@AutoFilter_Robot",
        "source_id": None,
        "prefix": "",
        "block": ["save the file", "will be deleted", "select language"],
        "block_url": ["LfvtadGw", "terabox"]
    },
    {
        "name": "LtMovie",
        "token": "8808014809:AAEacf05HWO2g4HFWDTlP8IC6lXMBxILqbM",
        "session": "1AZWarzgBu7jej2sCVzECGYhhyLC6ZPpyuIhEVSVXQ7QvYEH1_VpohEG5trvsjNiKBwpEYT1EK2oatfxVmR0WlGrQmvzEsl-uEhbLNmxP7mmEMtxcxLbICa4IYJZdjugBdyyJw89zGH_hqBE3vwCcoEH76R-Mc1TK6ODGhgJMBUqvn-b95kkujG1CcvZhv3ddjR8_Hd_ZVNaJBCyUtTQMTqGGfFYgXzymuoFrTEF8Vsinl9-OfukCbnO3dLMS4AtmZ72qo51SnTk144LLrtVzBTndd5I8XcQ2ab8zGQdNhMXVCFsR4ddwAXI2JfFWA2iUw7KjnROJ7k9EiQR1zZiKKt3s6-d4WV4=",
        "source": "@Lt_Moviebot",
        "source_id": 8504453537,
        "prefix": "",
        "block": [],
        "block_url": ["d-3RL7TJKnVlN2Nk", "CM_Zone", "f9RVIwfGDYo2NDM1", "LfvtadGw"],
        "footer": "\n\n➠ @BuddyMovies_official\n➠ @BuddyMovies_Bot",
        "no_url": True
    },
    {
        "name": "Angela",
        "token": "8894814453:AAGAuF3cjETqYt_mY2os9raZgMxSZtFqD_E",
        "session": "1AZWarzgBu7jej2sCVzECGYhhyLC6ZPpyuIhEVSVXQ7QvYEH1_VpohEG5trvsjNiKBwpEYT1EK2oatfxVmR0WlGrQmvzEsl-uEhbLNmxP7mmEMtxcxLbICa4IYJZdjugBdyyJw89zGH_hqBE3vwCcoEH76R-Mc1TK6ODGhgJMBUqvn-b95kkujG1CcvZhv3ddjR8_Hd_ZVNaJBCyUtTQMTqGGfFYgXzymuoFrTEF8Vsinl9-OfukCbnO3dLMS4AtmZ72qo51SnTk144LLrtVzBTndd5I8XcQ2ab8zGQdNhMXVCFsR4ddwAXI2JfFWA2iUw7KjnROJ7k9EiQR1zZiKKt3s6-d4WV4=",
        "source": "@Angela2_moviebot",
        "source_id": 8143714699,
        "prefix": "",
        "block": [],
        "footer": "\n\n➠ @BuddyMovies_official\n➠ @BuddyMovies_Bot",
        "no_url": True,
        "handle_start": True
    },
    {
        "name": "Apple",
        "token": "8760379291:AAHHIOGgqTJT0IINcM4dNV2bOYDXHfV0r7I",
        "session": "1AZWarzgBu7jej2sCVzECGYhhyLC6ZPpyuIhEVSVXQ7QvYEH1_VpohEG5trvsjNiKBwpEYT1EK2oatfxVmR0WlGrQmvzEsl-uEhbLNmxP7mmEMtxcxLbICa4IYJZdjugBdyyJw89zGH_hqBE3vwCcoEH76R-Mc1TK6ODGhgJMBUqvn-b95kkujG1CcvZhv3ddjR8_Hd_ZVNaJBCyUtTQMTqGGfFYgXzymuoFrTEF8Vsinl9-OfukCbnO3dLMS4AtmZ72qo51SnTk144LLrtVzBTndd5I8XcQ2ab8zGQdNhMXVCFsR4ddwAXI2JfFWA2iUw7KjnROJ7k9EiQR1zZiKKt3s6-d4WV4=",
        "source": "@Apple_moviebot",
        "source_id": 8104769075,
        "prefix": "",
        "block": [],
        "footer": "\n\n❤️ @BuddyMovies_Bot",
        "no_url": True,
        "pending_file": True
    },
    {
        "name": "ChatGPT",
        "token": "8952066629:AAHLnoIl62kY0wf4XrFWKiiDq9UaNbjk9zE",
        "session": "1AZWarzgBu7jej2sCVzECGYhhyLC6ZPpyuIhEVSVXQ7QvYEH1_VpohEG5trvsjNiKBwpEYT1EK2oatfxVmR0WlGrQmvzEsl-uEhbLNmxP7mmEMtxcxLbICa4IYJZdjugBdyyJw89zGH_hqBE3vwCcoEH76R-Mc1TK6ODGhgJMBUqvn-b95kkujG1CcvZhv3ddjR8_Hd_ZVNaJBCyUtTQMTqGGfFYgXzymuoFrTEF8Vsinl9-OfukCbnO3dLMS4AtmZ72qo51SnTk144LLrtVzBTndd5I8XcQ2ab8zGQdNhMXVCFsR4ddwAXI2JfFWA2iUw7KjnROJ7k9EiQR1zZiKKt3s6-d4WV4=",
        "source": "@gpt3ru_chat_bot",
        "source_id": 6157862059,
        "prefix": "",
        "block": ["please wait"],
        "is_chatgpt": True
    }
]

os.environ['PYTHONOPTIMIZE'] = '2'
gc.set_threshold(5000, 50, 50)

processed_msgs = set()

class Bridge:
    def __init__(self, c):
        self.c = c
        self.sessions = OrderedDict()
        self.results = {}
        self.bmap = {}
        self.rl = {}
        self.pending = None
        self.queue = deque()
        self.bot = TelegramClient(f'b_{c["name"]}', API_ID, API_HASH, retry_delay=3, auto_reconnect=True, timeout=15)
        self.usr = TelegramClient(StringSession(c["session"]), API_ID, API_HASH, retry_delay=3, auto_reconnect=True, timeout=15)

    def clean(self):
        if len(processed_msgs) > 500: processed_msgs.clear()
        now = time.time()
        for k in [k for k, v in self.sessions.items() if now - v.get('t', 0) > 300]: self.sessions.pop(k, None)
        if len(self.results) > 100:
            for k in list(self.results.keys())[:50]: self.results.pop(k, None)
        if len(self.bmap) > 2000:
            for k in list(self.bmap.keys())[:1000]: self.bmap.pop(k, None)
        if self.c.get("is_chatgpt") and len(self.queue) > 100:
            for _ in range(50): self.queue.popleft()
        gc.collect()

    def rl_check(self, uid):
        now = time.time()
        limit = 10 if self.c.get("is_chatgpt") else 15
        if uid in self.rl:
            recent = [t for t in self.rl[uid] if now - t < 60]
            self.rl[uid] = recent
            if len(recent) >= limit: return False
        else: self.rl[uid] = []
        self.rl[uid].append(now)
        return True

    def clean_text(self, txt):
        if not txt: return txt
        txt = re.sub(r'https?://\S+', '', txt)
        txt = re.sub(r'@\w+', '', txt)
        txt = re.sub(r'.*[Uu]pdates?\s*:.*', '', txt)
        txt = re.sub(r'.*auto.?delete.*', '', txt, flags=re.IGNORECASE)
        txt = re.sub(r'.*copyright.*', '', txt, flags=re.IGNORECASE)
        txt = re.sub(r'Hey \*\*.*?\*\*!?', '', txt)
        txt = re.sub(r'Search Query:', '🔍', txt)
        txt = re.sub(r'Total Results:', '📊', txt)
        txt = re.sub(r'Page:', '📄', txt)
        txt = re.sub(r'\n\s*\n\s*\n', '\n\n', txt)
        return txt.strip()

    def build_btns(self, msg, chat, mid):
        if not msg or not msg.buttons: return None
        btns, dmap = [], {}
        block_url = self.c.get("block_url", [])
        no_url = self.c.get("no_url", False)
        skip_btn = self.c.get("skip_btn", [])
        
        for ri, row in enumerate(msg.buttons):
            r = []
            for bi, btn in enumerate(row):
                txt = (btn.text or '').strip()
                if skip_btn and txt and any(s in txt.lower() for s in skip_btn): continue
                
                if btn.url:
                    if any(b in (btn.url or '') for b in block_url): continue
                    if self.c.get("handle_start") and 'start=' in btn.url:
                        p = parse_qs(urlparse(btn.url).query)
                        sd = p.get('start', [''])[0]
                        if sd:
                            fd = f"dl_{sd[:40]}"
                            dmap[fd] = (msg.id, ri, bi, sd)
                            r.append(Button.inline(txt[:50] if txt else '📥', fd))
                        continue
                    if no_url: continue
                    r.append(Button.url(txt[:50], btn.url))
                elif btn.data:
                    data = btn.data.decode() if isinstance(btn.data, bytes) else btn.data
                    dmap[data] = (msg.id, ri, bi, None)
                    if txt in ['\u200b', '\u200b ']:
                        ds = str(btn.data)
                        if 'lang' in ds: txt = '🌐'
                        elif 'qual' in ds: txt = '🎞️'
                        elif 'next' in ds or 'nxt' in ds: txt = '▶️'
                        elif 'pgkb' in ds or 'buttons' in ds: txt = '📄'
                        else: txt = '▫️'
                    r.append(Button.inline(txt[:50] if txt else '📥', data[:64]))
            if r: btns.append(r)
        if dmap: self.bmap[(chat, mid)] = dmap
        return btns if btns else None

    async def on_new(self, event):
        self.clean()
        m = event.message
        if m.id in processed_msgs:
            processed_msgs.add(m.id)
            return
        processed_msgs.add(m.id)
        sid = self.c.get("source_id")
        if sid:
            if m.sender_id != sid: return
        elif not m.sender or not m.sender.bot: return
        
        txt = m.text or ''
        if any(x in txt.lower() for x in self.c.get("block", [])): return
        
        if self.c.get("is_chatgpt"):
            if self.queue and txt:
                uid, name, rid = self.queue.popleft()
                clean = self.clean_text(txt)
                try: await self.bot.send_message(GRUPO, f"🤖 **{name}:**\n\n{clean[:2000]}", reply_to=rid)
                except: await self.bot.send_message(GRUPO, f"🤖 **{name}:**\n\n{clean[:2000]}")
            return
        
        if self.c.get("pending_file") and self.pending:
            if m.media and not m.photo:
                uid, name, rid = self.pending
                self.pending = None
                cap = self.clean_text(txt) + self.c.get("footer", "")
                sent = await self.usr.send_file(CANAL, m.media, caption=cap)
                link = f"https://t.me/{CANAL[1:]}/{sent.id}"
                await self.bot.send_message(GRUPO, f"🎬 **{name}**\n\n🔗 {link}", buttons=[[Button.url("🎥 VER CONTENIDO", link)]], reply_to=rid)
                return
        
        if not self.sessions: return
        uid = list(self.sessions.keys())[-1]
        s = self.sessions[uid]
        name = s.get('name', 'Usuario')
        rid = s.get('rid')
        tchat = s.get('chat', GRUPO) if not sid else GRUPO
        
        if m.media:
            raw = self.clean_text(txt)
            if self.c.get("footer"): raw += self.c["footer"]
            sent = await self.usr.send_file(CANAL, m.media, caption=raw)
            link = f"https://t.me/{CANAL[1:]}/{sent.id}"
            title = raw.split('\n')[0][:80] if raw else "Archivo"
            await self.bot.send_message(tchat, f"🎬 **{name}**\n📁 {title}\n\n🔗 {link}", buttons=[[Button.url("🎥 VER CONTENIDO", link)]], link_preview=False, reply_to=rid)
        
        elif txt and m.buttons and len(txt) > 15:
            cleaned = self.clean_text(txt)
            if not cleaned: return
            sent = await self.bot.send_message(tchat, "...", reply_to=rid)
            oid = sent.id
            btns = self.build_btns(m, tchat, oid)
            if (tchat, None) in self.bmap: self.bmap[(tchat, oid)] = self.bmap.pop((tchat, None))
            await self.bot.edit_message(tchat, oid, cleaned[:4000], buttons=btns)
            self.results[m.id] = (tchat, oid)

    async def on_edit(self, event):
        self.clean()
        m = event.message
        sid = self.c.get("source_id")
        if sid:
            if m.sender_id != sid: return
        elif not m.sender or not m.sender.bot or not m.text: return
        
        txt = m.text or ''
        if any(x in txt.lower() for x in self.c.get("block", [])): return
        if not txt or not m.buttons: return
        
        cleaned = self.clean_text(txt)
        if not cleaned: return
        
        if m.id in self.results:
            chat, mid = self.results[m.id]
            btns = self.build_btns(m, chat, mid)
            try: await self.bot.edit_message(chat, mid, cleaned[:4000], buttons=btns); return
            except: pass
        
        if not self.sessions: return
        uid = list(self.sessions.keys())[-1]
        s = self.sessions[uid]
        tchat = s.get('chat', GRUPO) if not sid else GRUPO
        
        sent = await self.bot.send_message(tchat, "...", reply_to=s.get('rid'))
        oid = sent.id
        btns = self.build_btns(m, tchat, oid)
        if (tchat, None) in self.bmap: self.bmap[(tchat, oid)] = self.bmap.pop((tchat, None))
        await self.bot.edit_message(tchat, oid, cleaned[:4000], buttons=btns)
        self.results[m.id] = (tchat, oid)

    async def on_msg(self, event):
        self.clean()
        if event.is_private:
            await event.reply("🎬 <b>¡BuddyPelis!</b>\n\n📽️ <b>+5 millones de películas y series</b>\n🔍 Busca sin límites en el grupo\n\n👉 <b>Únete:</b> @BuddyMovies_official", buttons=[[Button.url("🎥 IR AL GRUPO", "https://t.me/BuddyMovies_official")]], link_preview=False)
            return
        if event.out or not event.text: return
        q = event.text.strip()
        if len(q) < 2 or q.startswith("/"): return
        if not self.rl_check(event.sender_id): return
        try: s = await event.get_sender(); name = s.first_name if s else "Usuario"
        except: name = "Usuario"
        self.sessions[event.sender_id] = {'name': name, 'chat': event.chat_id, 'rid': event.message.id, 't': time.time()}
        if self.c.get("is_chatgpt"):
            self.queue.append((event.sender_id, name, event.message.id))
        await self.usr.send_message(self.c["source"], f"{self.c.get('prefix', '')}{q}")

    async def on_click(self, event):
        data = event.data.decode() if isinstance(event.data, bytes) else event.data
        if not data: return
        sub = self.bmap.get((event.chat_id, event.message_id))
        if sub and data in sub:
            info = sub[data]
            sp = info[3] if len(info) > 3 else None
            if sp:
                await event.answer("⚡ Solicitando...")
                await self.usr.send_message(self.c["source"], f"/start {sp}")
                return
            if self.c.get("pending_file") and self.sessions:
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
        await event.answer("⏳ Expiró")

    async def heartbeat(self):
        while True:
            await asyncio.sleep(180)
            try: await self.bot.get_me(); await self.usr.get_me(); self.clean()
            except: pass

    async def start(self):
        await self.usr.start()
        await self.bot.start(bot_token=self.c["token"])
        self.usr.add_event_handler(self.on_new, events.NewMessage(chats=self.c["source"]))
        self.usr.add_event_handler(self.on_edit, events.MessageEdited(chats=self.c["source"]))
        self.bot.add_event_handler(self.on_msg, events.NewMessage)
        self.bot.add_event_handler(self.on_click, events.CallbackQuery)
        print(f"✅ {self.c['name']} → {GRUPO}")
        asyncio.create_task(self.heartbeat())
        await asyncio.gather(self.bot.run_until_disconnected(), self.usr.run_until_disconnected())

async def main():
    print(f"🚀 Iniciando {len(BRIDGES)} bridges...")
    tasks = [Bridge(c).start() for c in BRIDGES]
    await asyncio.gather(*tasks)

class H(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    def do_HEAD(self): self.send_response(200); self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), H).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

def keep_alive():
    while True:
        time.sleep(600)
        try: urllib.request.urlopen(f"http://localhost:{int(os.environ.get('PORT', 10000))}", timeout=5)
        except: pass

threading.Thread(target=keep_alive, daemon=True).start()

asyncio.run(main())
