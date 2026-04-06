import re
import sys
import asyncio
import subprocess
import platform
import json
import os
from PySide6 import QtCore, QtWidgets
from data.draggable_list import DraggableList
from data.menubar import set_menubar

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyPing")
        self.resize(370, 600)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(12, 0, 12, 12)
        layout.setSpacing(8)
        set_menubar(self)

        self.listw = DraggableList()
        layout.addWidget(self.listw)

        self._save_path = ".pyping_hosts.json"
        self.listw.list_changed.connect(self._on_list_changed)

        self.load_hosts()
        if self.listw.list.count() == 0:
            self.listw.add_host("127.0.0.1")

        self._loop = asyncio.get_event_loop()
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._pump_asyncio)
        self._timer.start(50)

        self._task = None
        self._start_ping_task()

    def _start_ping_task(self):
        task = getattr(self, "_task", None)
        if not task or task.done():
            self._task = asyncio.ensure_future(self.ping_loop())

    def _restart_ping_task(self):
        task = getattr(self, "_task", None)
        if task is not None and not task.done():
            task.cancel()
        self._start_ping_task()


    def _pump_asyncio(self):
        self._loop.call_soon(self._loop.stop)
        self._loop.run_forever()

    def blocking_ping_output(self, host: str, timeout: int = 3):
        system = platform.system().lower()
        if system == "windows":
            cmd = f"ping -n 1 -w {int(timeout*1000)} {host}"
        elif system == "darwin":
            cmd = f"ping -c 1 {host}"
        else:
            cmd = f"ping -c 1 -W {int(timeout)} {host}"
        try:
            out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=timeout + 1)
            return out.decode(errors="ignore")
        except subprocess.CalledProcessError as e:
            return e.output.decode(errors="ignore")
        except Exception:
            return None

    async def ping_host(self, host: str) -> float | None:
        loop = asyncio.get_running_loop()
        out = await loop.run_in_executor(None, self.blocking_ping_output, host, 3)
        if not out:
            return None
        m = re.search(r"time[=<]\s*([0-9]+(?:\.[0-9]+)?)\s*ms", out)
        return float(m.group(1)) if m else None

    async def ping_loop(self):
        try:
            while True:
                for row in list(self.listw.iterate_rows()):
                    if not row or not hasattr(row, "sig_set_latency"):
                        continue
                    host = row.host
                    lat = await self.ping_host(host)
                    try:
                        if lat is None:
                            row.sig_set_latency.emit("0 ms")
                            row.sig_set_status.emit(False)
                            row.sig_set_lost.emit(row.lost + 1)
                        else:
                            row.sig_set_latency.emit(f"{int(lat)} ms")
                            row.sig_set_status.emit(True)
                    except RuntimeError:
                        continue
                    await asyncio.sleep(0.05)
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            return

    def get_hosts_data(self):
        return [self.listw.list.item(i).data(QtCore.Qt.UserRole) for i in range(self.listw.list.count())]

    def save_hosts(self, path: str | None = None):
        p = path or self._save_path
        os.makedirs(os.path.dirname(p), exist_ok=True) if os.path.dirname(p) else None
        with open(p, "w", encoding="utf-8") as f:
            json.dump(self.get_hosts_data(), f, ensure_ascii=False, indent=2)

    def load_hosts(self, path: str | None = None):
        p = path or self._save_path
        if not os.path.exists(p):
            return
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return
        self.listw.list.clear()
        for entry in data:
            self.listw.add_host(entry.get("name"), entry.get("lost", 0))

    def _on_list_changed(self):
        try:
            self.save_hosts()
        except Exception:
            pass
        self._restart_ping_task()
