import asyncio
import os

from mitmproxy.options import Options
from mitmproxy.tools.web.master import WebMaster

from .misc import proxy_set
from . import config


class MitmproxyServer:
    def __init__(self, debug: bool):
        self.running = False
        self.task = None
        self.stopped = asyncio.Event()
        self.master = WebMaster  # if debug else Master
        self.m: WebMaster = self.master(opts=Options(), with_termlog=True)
        self.m.options.listen_host = "127.0.0.1"
        self.m.options.web_open_browser = False
        if debug:
            self.m.options.web_host = "0.0.0.0"
            self.m.options.web_open_browser = True
        self.m.options.listen_port = 1942

    def run_mitmproxy(self):
        try:
            closeFortnite: bool = config.read()["closeFortnite"]
            if closeFortnite:
                closeFortnite: bool = config.read()["closeFortnite"]
                if closeFortnite:
                    closeTasks: list[str] = [
                        "taskkill /f /im epicgameslauncher.exe > nul",
                        "taskkill /f /im FortniteClient-Win64-Shipping_EAC.exe > nul",
                        "taskkill /f /im FortniteClient-Win64-Shipping_BE.exe > nul",
                        "taskkill /f /im FortniteLauncher.exe > nul",
                        "taskkill /f /im FortniteClient-Win64-Shipping.exe > nul",
                        "taskkill /f /im EpicGamesLauncher.exe > nul",
                        "taskkill /f /im EasyAntiCheat.exe > nul",
                        "taskkill /f /im BEService.exe > nul",
                        "taskkill /f /im BEServices.exe > nul",
                        "taskkill /f /im BattleEye.exe > nul",
                        "Sc stop FortniteClient-Win64-Shipping_EAC",
                        "Sc stop FortniteClient-Win64-Shipping_BE",
                    ]
                    jointCommand: str = ""
                    for command in closeTasks:
                        jointCommand += command + " & "

                    os.system(jointCommand)
            self.task = asyncio.create_task(self.m.run())
        except KeyboardInterrupt:
            pass

    def start(self):
        self.running = True
        self.run_mitmproxy()
        proxy_set(enabled=True)
