"""Experimental iOS entry point for the real Porn Fetch backend."""
import os
from pathlib import Path
import sys
import traceback

os.environ.setdefault('QT_QUICK_BACKEND', 'rhi')
os.environ.setdefault('QSG_RHI_BACKEND', 'opengl')
os.environ.setdefault('QSG_RENDER_LOOP', 'basic')

# App source/resources stay in the bundle; logs and relative runtime files go
# into the app's writable data container.
working = Path.home() / 'Documents' / 'PornFetch'
working.mkdir(parents=True, exist_ok=True)
os.chdir(working)
sys.argv = ['PornFetch']
try:
    from src.backend.application import main
    print('PORN_FETCH_IOS_BACKEND_IMPORTED', sys.version, flush=True)
    main()
except BaseException:
    traceback.print_exc()
    raise
