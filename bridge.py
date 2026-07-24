import asyncio, re, os, threading, gc, time, urllib.request
from collections import OrderedDict, deque
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# ==================== CONFIGURACIÓN ====================
API_ID = 28074212
API_HASH = "b18dae908474a377684922f3e9d5b795"
CANAL = "@BuddyMovies_canal"
GRUPO = "@BuddyMovies_official"

BRIDGES = [
    {
        "name": "BuddyMovies",
        "token": "8984212389:AAFZMh_ZQZm8DlIqPLvQEljnC1UPVtRJV-Q",
        "session": "1AZWarzQBu5hWbHakw_V4c82HJA0uCNxvwdS_2JHHEVUbCghWQtCFrCbvfFEAMYTh1sCL3mMpTCJMmETKHXkmgBhynikL_1MTEXJfDlFxjnZQDXf1Glbd5w0HuyCQwEP6K_F2DnAS5vsGtH452l_HDS0uQMAGryhoTV7n5Tr9-5E1DmwY4CfKNV7uzYat15FQ6Nsm_vu8iPnQEwy5w5egiY_xnULhFKIkjWrr9gm7WS_OZbSwmEThy32o3I7zxIO__BiRmAFqPnICFo8OJR_FqU7JYoGvHeScnbgbOGU-bcmFUZrq_sFBbldOn1Y4G0TBw6gLeCCUjhwIh-td7KAjaDIRdaoI_lc=",
        "source": "@pooppuuui",
        "source_id": None,
        "prefix": "/search ",
        "block": ["buscando", "espera", "recuerda usar", "ayúdanos", "compártelo", "gracias"]
    },
    {
        "name": "BuddyNotify",
        "token": "8463069047:AAGeZg0IQd-1-Mv3ubxqnwZY1oJgxio9hr8",
        "session": "1AZWarzQBuzncKy_mbzKcjlq0_XeKVuhMaiHWMBs3kkt9hmss9EcHTh9f9RtgQYkoDx4oXfLs8rnlwzNA8AHxmt47X2J3r4YJr0QVNVzX3meQKnDv1EKsnctVofcPlsHGuXPZutTrhs0-rtMFXO8TYMESuLbcu0BlENZDA6LVWzItTe17yMvgWexGLJMIyhO-yIrRxHr4838YkKxdxUflsSkjtSZIV8W4EWtrd6eOcTcZbaQyJEUT6jcyXrePbmfaOjMoOsx1PJF1dQisoPP_C-mRSHgp59Za4LmBM4EqQgzXeoPdUdXFRDkCJAfjzc3p6lnU7HqEtcKmm2EIzY43vj_iKSroOOo=",
        "source": "@TlgramMovieSearch_Bot",
        "source_id": None,
        "prefix": "",
        "block": ["procesando", "espera", "maldito", "comparte", "terabox", "revisa el anuncio"],
        "skip_btn": ["compartir bot", "añadir a grupo", "menú principal", "share bot", "add to group", "main menu"]
    },
    {
        "name": "AutoFilter",
        "token": "7690330806:AAFAemkor12n71UAPaoJcnAcnPI_R_Xqygs",
        "session": "1AZWarzQBu2q3JnP8YtBiwtloyr8QVF6AOFug129qO5bNQIRLsvnGelrXXIRdVYezjgm0IJNH5d_3lIBSNTxBTQnSss_Oz_MQksUSw1883Vbx5O3RyUM6UhYxhPe9jNuCHFhfTPn3iwxlQ63tJiNJ_Dd7ndNYdDFKsnrnKDvOkGX6H6UZyABCKj25nq8MCp6LRs22lV-AkmmVkdPRwL2CF7bIosmIHnfOrA2VxO_8ozC-iB08xA19YEqQtbA6YxCcYVgQuJAAyqqRIhqtHSibUloyqzYiLGUX7wWKPjYOrGOI4X-_NJAmTlkIvtQQHwd1HKI6NVLjnLker7Nas0wwUja1lOCfpQI=",
        "source": "@AutoFilter_Robot",
        "source_id": None,
        "prefix": "",
        "block": ["save the file", "will be deleted", "select language"],
        "block_url": ["LfvtadGw", "terabox"]
    },
    {
        "name": "LtMovie",
        "token": "8808014809:AAEacf05HWO2g4HFWDTlP8IC6lXMBxILqbM",
        "session": "1AZWarzQBuw2Qy79iGpD5cWK5pf1LtqHo8f-gjYTl7G8c4wcEvAXuhRifBWgMyrQeXsW62Jpv2YbE3yQJJC1D520D4CPbkOHM5c9NUlDOaQNGDg4gbTzf00Ye6KlbLifZpgQI9Zk3SO9EeMJlq7MVvqUNUgMpCaxYl3oMcAhhqnzHPgMmdQR9epRSKMU6d_PeQ7NHThlpYHHYB5wpMBz2-IaajdMMXPB4-shgmIHGeh_BdQy6UArhkcLFaxCu-f60MK39MUzYq4UElN0aaSn7HuSfaszh5QlALJQe9AZrP1Jsa7UzErtsZ0JDsoMt6ujcvgpXCYu3xYQkNTQh1s7n-qb4y8uaQZU=",
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
        "session": "1AZWarzQBuw2Qy79iGpD5cWK5pf1LtqHo8f-gjYTl7G8c4wcEvAXuhRifBWgMyrQeXsW62Jpv2YbE3yQJJC1D520D4CPbkOHM5c9NUlDOaQNGDg4gbTzf00Ye6KlbLifZpgQI9Zk3SO9EeMJlq7MVvqUNUgMpCaxYl3oMcAhhqnzHPgMmdQR9epRSKMU6d_PeQ7NHThlpYHHYB5wpMBz2-IaajdMMXPB4-shgmIHGeh_BdQy6UArhkcLFaxCu-f60MK39MUzYq4UElN0aaSn7HuSfaszh5QlALJQe9AZrP1Jsa7UzErtsZ0JDsoMt6ujcvgpXCYu3xYQkNTQh1s7n-qb4y8uaQZU=",
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
        "session": "1AZWarzQBu3ZUy3OFCmSneDqRGmhmOequJNsxnU2U1n1U5gCumQo2B_7ve5en_f8KEmXMp7WUE-nWX3SnvxNuBG4xItjnz6L4rYVbZ-OhxEFX8WrF4PdGNXgWWqkgxlH9O7NEZfspmsiRd9QTE9WO0ZRhl-UcY9zXh_066TUxbsInY71vL-0GZjvHHGn1afy9Gj7nphO5h8ockeypg9Kx5bYOJ1bRki36iyrVNbUTpMfFiB4KkEAC1hFlqYoo56EEVEy7piw0TR2L3QDCZnahy3XI8Azpt0JPIc0Y5TZCDUcYyWQtkS5H_CKvnxVTIPitWadXZVHIrQRXz3Lj2KvF6ZyiYUESy0g=",
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
        "session": "1AZWarzsBu3ny9-HTgWpuIkTxb2vRDvQJu0tU-l_79zEFPRsg1fX4vV7aQw5Qew3KyFIi7-VuZDR3niQvGaXRh89KP2AywppMfdolEwgquZIRROPPNuLQovcl5hpp4vvt6r1gb6Zr1EZrOBOp4PKiG2RLff0b2bKWzRPd-pr5CbDPtTrIBSFMXnMCDwZvs8wxB6n1KZ6H6b5Ndunvr3yOhSKDfzqhWq8Rz3HpGq6iWo1vI418VFHbUXVvlGBe47jEDQc6eaosxAv1EFjRVbmumdQT7aF1GW3u-H_pfpRwpYQHb0r3hVBMCva6eDuTZ_L5rOaE2Zix41Z3C51umX6FZjdHGuyed20=",
        "source": "@gpt3ru_chat_bot",
        "source_id": 6157862059,
        "prefix": "",
        "block": ["please wait"],
        "is_chatgpt": True
    }
]

os.environ['PYTHONOPTIMIZE'] = '2'
gc.set_threshold(5000, 50, 50)

# ==================== BRIDGE CORREGIDO ====================
class Bridge:
    def __init__(self, c):
        self.c = c
        self.sessions = OrderedDict()  # user_id -> {name, chat, rid, t}
        self.bmap = {}  # (chat_id, msg_id, data) -> (orig_msg_id, row, col, start_param)
        self.rl = {}    # rate limit
        self.pending = None  # (uid, name, rid) para Apple
        self.queue = deque()  # para ChatGPT
        self.bot = TelegramClient(f'b_{c["name"]}', API_ID, API_HASH, retry_delay=3, auto_reconnect=True, timeout=15)
        self.usr = TelegramClient(StringSession(c["session"]), API_ID, API_HASH, retry_delay=3, auto_reconnect=True, timeout=15)

    def clean(self):
        now = time.time()
        expired = [k for k, v in self.sessions.items() if now - v.get('t', 0) > 300]
        for k in expired: self.sessions.pop(k, None)
        # Limpiar bmap viejo (más de 30 min)
        if len(self.bmap) > 3000:
            keys = list(self.bmap.keys())
            for k in keys[:1500]: self.bmap.pop(k, None)
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
        if not txt: return ""
        # Eliminar URLs
        txt = re.sub(r'https?://\S+', '', txt)
        # Eliminar @menciones
        txt = re.sub(r'@\w+', '', txt)
        # Quitar frases publicitarias
        txt = re.sub(r'(?i).*updates?\s*:.*', '', txt)
        txt = re.sub(r'(?i).*auto.?delete.*', '', txt)
        txt = re.sub(r'(?i).*copyright.*', '', txt)
        txt = re.sub(r'(?i).*save\s+the\s+file.*', '', txt)
        txt = re.sub(r'(?i).*will\s+be\s+deleted.*', '', txt)
        txt = re.sub(r'(?i).*join\s+@\w+.*', '', txt)
        txt = re.sub(r'(?i).*share\s+(bot|and|&).*', '', txt)
        # Reemplazar "Hey **Nombre**!"
        txt = re.sub(r'Hey \*\*.*?\*\*!?', '👋 **¡Hola!**', txt)
        # Traducciones
        txt = txt.replace('Search Query:', '🔍 Búsqueda:')
        txt = txt.replace('Total Results:', '📊 Resultados:')
        txt = txt.replace('Page:', '📄 Página:')
        # Limpiar saltos de línea múltiples
        txt = re.sub(r'\n\s*\n\s*\n', '\n\n', txt)
        return txt.strip()

    def build_btns(self, msg, chat_id, msg_id):
        """Construye botones y guarda mapeo en bmap con clave (chat_id, msg_id, data)"""
        if not msg or not msg.buttons: return None
        btns = []
        block_url = self.c.get("block_url", [])
        no_url = self.c.get("no_url", False)
        skip_btn = self.c.get("skip_btn", [])
        
        for ri, row in enumerate(msg.buttons):
            r = []
            for bi, btn in enumerate(row):
                txt = (btn.text or '').strip()
                
                # Saltar botones no deseados
                if skip_btn and txt and any(s in txt.lower() for s in skip_btn): continue
                
                if btn.url:
                    if any(b in (btn.url or '') for b in block_url): continue
                    # Manejar botones start= (Angela)
                    if self.c.get("handle_start") and 'start=' in btn.url:
                        p = parse_qs(urlparse(btn.url).query)
                        sd = p.get('start', [''])[0]
                        if sd:
                            fd = f"st_{sd[:40]}"
                            self.bmap[(chat_id, msg_id, fd)] = (msg.id, ri, bi, sd)
                            r.append(Button.inline(txt[:50] if txt else '📥', fd))
                        continue
                    if no_url: continue
                    r.append(Button.url(txt[:50], btn.url))
                    
                elif btn.data:
                    data = btn.data.decode() if isinstance(btn.data, bytes) else btn.data
                    self.bmap[(chat_id, msg_id, data)] = (msg.id, ri, bi, None)
                    
                    # Botones invisibles -> emojis
                    if txt in ['\u200b', '\u200b ']:
                        ds = str(btn.data)
                        if 'lang' in ds: txt = '🌐'
                        elif 'qual' in ds: txt = '🎞️'
                        elif 'next' in ds or 'nxt' in ds: txt = '▶️'
                        elif 'pgkb' in ds or 'buttons' in ds: txt = '📄'
                        else: txt = '▫️'
                    
                    r.append(Button.inline(txt[:50] if txt else '📥', data[:64]))
            if r: btns.append(r)
        return btns if btns else None

    async def forward_result(self, m, uid, name, rid, tchat):
        """Envía/edita un resultado al grupo SIN DUPLICAR"""
        txt = m.text or ''
        
        # Si es archivo
        if m.media and not self.c.get("is_chatgpt"):
            raw = self.clean_text(txt)
            if self.c.get("footer"): raw += self.c["footer"]
            sent = await self.usr.send_file(CANAL, m.media, caption=raw)
            link = f"https://t.me/{CANAL[1:]}/{sent.id}"
            title = raw.split('\n')[0][:80] if raw else "Archivo"
            await self.bot.send_message(
                tchat,
                f"🎬 **{name}**\n📁 {title}\n\n🔗 {link}",
                buttons=[[Button.url("🎥 VER CONTENIDO", link)]],
                link_preview=False,
                reply_to=rid
            )
            return
        
        # Si es texto con botones
        if txt and m.buttons and len(txt) > 15:
            cleaned = self.clean_text(txt)
            if not cleaned: return
            
            # Enviar placeholder y editar con botones reales
            sent = await self.bot.send_message(tchat, "⏳", reply_to=rid)
            oid = sent.id
            btns = self.build_btns(m, tchat, oid)
            
            # Verificar que no se duplique el mensaje
            try:
                await self.bot.edit_message(tchat, oid, cleaned[:4000], buttons=btns)
            except Exception as e:
                # Si falla la edición, reenviar
                await self.bot.send_message(tchat, cleaned[:4000], buttons=btns, reply_to=rid)

    async def on_new(self, event):
        self.clean()
        m = event.message
        sid = self.c.get("source_id")
        txt = m.text or ''
        
        # Verificar origen
        if sid:
            if m.sender_id != sid: return
        elif not m.sender or not m.sender.bot: return
        
        # Bloquear frases
        if any(x in txt.lower() for x in self.c.get("block", [])): return
        
        # Bloquear "no encontrado"
        if re.search(r'no\s+(se\s+encontr|results?|found|available)', txt, re.IGNORECASE): return
        
        # ChatGPT
        if self.c.get("is_chatgpt"):
            if self.queue and txt:
                uid, name, rid = self.queue.popleft()
                clean = self.clean_text(txt)
                await self.bot.send_message(GRUPO, f"🤖 **{name}:**\n\n{clean[:2000]}", reply_to=rid)
            return
        
        # Apple: archivo pendiente después de click
        if self.c.get("pending_file") and self.pending:
            if m.media and not m.photo:
                uid, name, rid = self.pending
                self.pending = None
                cap = self.clean_text(txt) + self.c.get("footer", "")
                sent = await self.usr.send_file(CANAL, m.media, caption=cap)
                link = f"https://t.me/{CANAL[1:]}/{sent.id}"
                await self.bot.send_message(
                    GRUPO,
                    f"🎬 **{name}**\n\n🔗 {link}",
                    buttons=[[Button.url("🎥 VER CONTENIDO", link)]],
                    reply_to=rid
                )
                return
        
        if not self.sessions: return
        
        # Usar la sesión MÁS RECIENTE
        uid = list(self.sessions.keys())[-1]
        s = self.sessions[uid]
        name = s.get('name', 'Usuario')
        rid = s.get('rid')
        tchat = GRUPO  # Siempre al grupo para evitar duplicados
        
        await self.forward_result(m, uid, name, rid, tchat)

    async def on_edit(self, event):
        """Maneja ediciones del bot fuente"""
        self.clean()
        m = event.message
        sid = self.c.get("source_id")
        txt = m.text or ''
        
        if sid:
            if m.sender_id != sid: return
        elif not m.sender or not m.sender.bot or not txt: return
        
        if any(x in txt.lower() for x in self.c.get("block", [])): return
        if re.search(r'no\s+(se\s+encontr|results?|found|available)', txt, re.IGNORECASE): return
        if not txt or not m.buttons: return
        
        if not self.sessions: return
        uid = list(self.sessions.keys())[-1]
        s = self.sessions[uid]
        tchat = GRUPO
        
        cleaned = self.clean_text(txt)
        if not cleaned: return
        
        # Buscar si ya enviamos este mensaje y editarlo
        # Enviamos uno nuevo con los botones actualizados
        sent = await self.bot.send_message(tchat, "⏳", reply_to=s.get('rid'))
        oid = sent.id
        btns = self.build_btns(m, tchat, oid)
        await self.bot.edit_message(tchat, oid, cleaned[:4000], buttons=btns)

    async def on_msg(self, event):
        self.clean()
        if event.is_private:
            await event.reply(
                "🎬 <b>¡BuddyPelis!</b>\n\n"
                "📽️ <b>+5 millones de películas y series</b>\n"
                "🔍 Busca sin límites en el grupo\n\n"
                "👉 <b>Únete:</b> @BuddyMovies_official",
                buttons=[[Button.url("🎥 IR AL GRUPO", "https://t.me/BuddyMovies_official")]],
                link_preview=False
            )
            return
        
        if event.out or not event.text: return
        q = event.text.strip()
        if len(q) < 2 or q.startswith("/"): return
        
        if not self.rl_check(event.sender_id):
            try: await event.reply("⏳ Espera un momento...")
            except: pass
            return
        
        try:
            s = await event.get_sender()
            name = s.first_name if s else "Usuario"
        except:
            name = "Usuario"
        
        # Guardar sesión
        self.sessions[event.sender_id] = {
            'name': name,
            'chat': event.chat_id,
            'rid': event.message.id,
            't': time.time()
        }
        
        if self.c.get("is_chatgpt"):
            self.queue.append((event.sender_id, name, event.message.id))
        
        # Enviar búsqueda al bot fuente
        await self.usr.send_message(self.c["source"], f"{self.c.get('prefix', '')}{q}")

    async def on_click(self, event):
        """Maneja clicks en botones - SIN EXPIRAR"""
        data = event.data.decode() if isinstance(event.data, bytes) else event.data
        if not data: return
        
        chat_id = event.chat_id
        msg_id = event.message_id
        
        # Buscar en bmap con la clave correcta
        key = (chat_id, msg_id, data)
        if key in self.bmap:
            info = self.bmap[key]
            orig_msg_id, row, col, start_param = info
            
            # Si tiene start_param (Angela)
            if start_param:
                await event.answer("⚡ Solicitando...")
                await self.usr.send_message(self.c["source"], f"/start {start_param}")
                return
            
            # Si es Apple, preparar pending
            if self.c.get("pending_file") and self.sessions:
                uid = list(self.sessions.keys())[-1]
                s = self.sessions[uid]
                self.pending = (uid, s['name'], s['rid'])
            
            # Hacer click en el botón original
            try:
                msgs = await self.usr.get_messages(self.c["source"], ids=[orig_msg_id])
                if msgs and msgs[0].buttons:
                    await event.answer("⚡")
                    await msgs[0].buttons[row][col].click()
                    return
            except Exception as e:
                pass
        
        # Fallback: buscar en últimos 50 mensajes del bot fuente
        try:
            async for m in self.usr.iter_messages(self.c["source"], limit=50):
                if m.buttons:
                    for row in m.buttons:
                        for btn in row:
                            bd = btn.data.decode() if isinstance(btn.data, bytes) else btn.data
                            if bd == data:
                                # Guardar en bmap para futuro
                                self.bmap[(chat_id, msg_id, data)] = (m.id, 
                                    m.buttons.index(row), row.index(btn), None)
                                await event.answer("⚡")
                                await btn.click()
                                return
        except: pass
        
        await event.answer("⏳ Expiró")

    async def heartbeat(self):
        while True:
            await asyncio.sleep(180)
            try:
                await self.bot.get_me()
                await self.usr.get_me()
                self.clean()
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

# ==================== MAIN ====================
async def main():
    print(f"🚀 Iniciando {len(BRIDGES)} bridges corregidos...")
    tasks = [Bridge(c).start() for c in BRIDGES]
    await asyncio.gather(*tasks)

# ==================== SERVIDOR HTTP ====================
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), H).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

def keep_alive():
    while True:
        time.sleep(600)
        try:
            port = int(os.environ.get("PORT", 10000))
            urllib.request.urlopen(f"http://localhost:{port}", timeout=5)
        except: pass

threading.Thread(target=keep_alive, daemon=True).start()

asyncio.run(main())
