import asyncio, os, threading, time, urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

async def main():
    scripts = [
        "bridge_b1.py", "bridge_b2.py", "bridge_b3.py", "bridge_b4.py",
        "bridge_b5.py", "bridge_b6.py", "bridge_b7.py"
    ]
    processes = []
    for s in scripts:
        p = await asyncio.create_subprocess_exec("python3", s)
        processes.append(p)
        print(f"✅ {s} iniciado")
    
    await asyncio.gather(*[p.wait() for p in processes])

class H(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")

threading.Thread(target=lambda: HTTPServer(("0.0.0.0", int(os.environ.get("PORT",10000))), H).serve_forever(), daemon=True).start()

def ka():
    while True:
        time.sleep(600)
        try: urllib.request.urlopen(f"http://localhost:{int(os.environ.get('PORT',10000))}", timeout=5)
        except: pass
threading.Thread(target=ka, daemon=True).start()

asyncio.run(main())
