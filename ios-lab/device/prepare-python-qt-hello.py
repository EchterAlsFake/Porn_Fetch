from pathlib import Path
import os
import subprocess

device = Path(__file__).resolve().parent
lab = device.parent
app = device / "python-qt-hello"
env = os.environ.copy()
env["DEVELOPER_DIR"] = "/Users/asuna/Downloads/Xcode.app/Contents/Developer"
env["PATH"] = str(lab / ".venv/bin") + ":/usr/local/bin:/usr/bin:/bin"
subprocess.run([str(lab / ".venv/bin/pyside6-ios-deploy"), str(app / "main.py"),
    "--name", "PythonQtPhoneHello", "--bundle-id", "local.asuna.PythonQtPhoneHello",
    "--wheel-pyside", str(next((device / "wheels").glob("pyside6-*.whl"))),
    "--wheel-shiboken", str(next((device / "wheels").glob("shiboken6-*.whl")))],
    cwd=app, env=env, check=True)
