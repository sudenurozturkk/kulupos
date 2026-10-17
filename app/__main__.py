"""python -m app  →  http://127.0.0.1:8000"""
import os
import threading
import webbrowser

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PANO_PORT", "8000"))
    if not os.environ.get("PANO_NO_BROWSER"):
        threading.Timer(1.5, webbrowser.open, (f"http://127.0.0.1:{port}",)).start()
    # 127.0.0.1 on purpose: the board never listens on the network.
    uvicorn.run("app.main:app", host="127.0.0.1", port=port)
