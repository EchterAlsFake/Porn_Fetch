"""Physical iPhone entry point for the real Porn Fetch application."""
import os
from pathlib import Path
import sys
import traceback

working = Path.home() / "Documents/PornFetch"
working.mkdir(parents=True, exist_ok=True)
os.chdir(working)
sys.stdout = (working / "ios-runtime.log").open("w", buffering=1)
sys.stderr = sys.stdout
sys.argv = ["PornFetch"]

from PySide6.QtCore import qInstallMessageHandler
qInstallMessageHandler(lambda kind, context, message: print(message, flush=True))

try:
    from src.backend.application import main
    print("PORN_FETCH_IPHONE_BACKEND_IMPORTED", sys.version, flush=True)
    if (working / "ios-remux-job.json").is_file():
        import threading
        from ios_remux_check import run
        threading.Thread(target=run, args=(working,), daemon=True).start()
    main()
except BaseException:
    traceback.print_exc()
    raise
