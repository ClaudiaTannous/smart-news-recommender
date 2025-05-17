import uvicorn
import os
import webbrowser
import threading
import time

def open_browser():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:8000/recommend-news-page")  # for local only

if __name__ == "__main__":
    # ✅ Ensure working directory is project root (where static/ and templates/ live)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    port = int(os.environ.get("PORT", 8000))  # Cloud Run injects PORT
    threading.Thread(target=open_browser).start()
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
