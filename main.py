import asyncio
import ssl
import os
import sys
import threading
import webbrowser
import aiohttp
from cryptography import x509
from cryptography.hazmat.primitives import hashes

import webview
import subprocess
import json
import urllib.parse

from mitmproxy import certs
from multiprocessing.connection import Connection
from multiprocessing.connection import Client

# Other Local Imports
import apis
import type_definitions
import constants

from utils import config
from utils.misc import proxy_set
from utils.misc import updateRPC, connectRPC
from utils import discord
from utils.translation import init_translations

from api import checkDiscord

import functools

userSettings: type_definitions.defaultUserSettings = {
    "status": f"👉 discord.gg/fortnitedev 🔌",
    "useStatus": True,
    "lockerId": "",
    "premium": False,
    "deploymentId": "",
    "launcherToken": "",
    "displayName": "",
    "configDisplayName": "",
    "updatedTime": "",
    "creationTime": "",
    "athenaItemId": "",
    "pipe": 0,
    "member": False,
    "banned": False,
    "accountId": "",
    "translations": None,
    "badges": [],
    "replaceText": True,
    "language": "en",
    "discordAccountId": "",
    "jid": "",
    "accountId": "",
    "xmppFlow": None,
    "debug": False,
    "savedUrl": None,
}
htmls = ""


async def getHTMLFiles(session: aiohttp.ClientSession):
    async with session.get(f"{constants.URLs.CDN}/ui/1.2.0.html") as resp:
        return await resp.text(encoding="utf-8")


def beforeStart(loop: asyncio.AbstractEventLoop):
    apis.updateUserBadges(userSettings["badges"])
    if userSettings["premium"] == True:
        apis.togglePremium(enabled=True)

    loop.create_task(updateRPC(userSettings))
    proxy_set(enabled=False)


async def updateUsers(session: aiohttp.ClientSession):
    async with session.get(f"{constants.URLs.COMMANDO}/users") as resp:
        users = await resp.text()
    webview.windows[0].evaluate_js(f"setUserCount({users})")


def beforeClose():
    proxy_set(enabled=False)
    closeFortnite: bool = config.read()["closeFortnite"]
    if closeFortnite:
        jointCommand: str = ""
        for command in constants.closeTasks:
            jointCommand += command + " & "

        os.system(jointCommand)
    return


def cert_installed():
    fingerprint = certs.CertStore.from_store(
        path=os.path.expanduser("~/.mitmproxy/"), basename="mitmproxy", key_size=2048
    ).default_ca.fingerprint()
    return any(
        x509.load_der_x509_certificate(cert).fingerprint(hashes.SHA256()) == fingerprint
        for cert, _, _ in ssl.enum_certificates("ROOT")
    )


async def init(loop: asyncio.AbstractEventLoop, session: aiohttp.ClientSession):
    await init_translations(session)
    await connectRPC()
    global htmls
    htmls = await getHTMLFiles(session)

    defaultConfig: type_definitions.Config = {
        "configVersion": constants.currentConfigVersion,
        "tosAgreed": False,
        "closeFortnite": True,
        "updateSkip": False,
        "InviteExploit": {"users": []},
        "saved": {
            "presets": {},
            "favorite": [],
            "archived": [],
        },
        "extraSettings": {
            "lang": "en",
            "video": f"https://www.youtube.com/watch?v=deBwYZnMJtg",
            "status": "👉 discord.gg/fortnitedev 🔌",
            "image": f"{constants.URLs.CDN}/SplashScreen.png",
            "radio_enabled": True,
            "playlist": "playlist_nobuildbr_squads",
            "images_enabled": True,
            "nigga_enabled": True,
            "display_name": "",
            "replacements_enabled": True,
            "vbucks": 99999999999999999,
            "crowns": 69420,
            "battlestars": 69420,
            "levels": 999,
        },
        "WebSocketLogging": False,
        "refreshToken": "",
    }

    if not os.path.exists(constants.configDir):
        os.mkdir(constants.configDir)

    if not os.path.exists(constants.configFilePath):
        with open(constants.configFilePath, "w") as f:
            json.dump(defaultConfig, f, indent=2)

    if (
        len(sys.argv) >= 2
        and (uri := urllib.parse.urlparse(sys.argv[1])).scheme == "boogie"
    ):
        print("[+] Launched via URL")
        if uri.netloc == "authorize" and "code" in (
            query := urllib.parse.parse_qs(uri.query)
        ):
            connection: Connection = Client(
                constants.address, authkey=constants.authkey
            )
            connection.send(query["code"][0])
            connection.close()
            sys.exit(0)
    elif "-debug" in sys.argv:
        print("[+] Debugging")
        userSettings["debug"] = True

    linkedDiscord = False
    try:
        refreshToken: str | None = config.read().get("refreshToken", None)
        print(refreshToken)
        assert refreshToken
        linkedDiscord = True
        access_token, refresh_token = await discord.get_access_token(session, refreshToken)
        config_data: type_definitions.Config = config.read()
        config_data["refreshToken"] = refresh_token

        with open(constants.configFilePath, "w") as f:
            json.dump(config_data, f, indent=2)
        await checkDiscord(session, access_token, userSettings)
    except AssertionError:
        print("[-] No refresh token found")

    if not userSettings["member"] and linkedDiscord:
        webbrowser.open_new_tab("https://discord.gg/fortnitedev")
        sys.exit(1)

    window: webview.Window = webview.create_window(
        title=constants.title,
        html=htmls,
        # url="http://localhost:5173",
        js_api=apis.Api(loop, session, userSettings),
        frameless=True,
        resizable=False,
        vibrancy=True,
        width=1000,
        height=675,
        easy_drag=False,
        text_select=True,
    )
    window.events.closing += beforeClose
    window.events.loaded += functools.partial(beforeStart, loop)
    webview.settings = {
        "ALLOW_DOWNLOADS": False,
        "ALLOW_FILE_URLS": True,
        "OPEN_EXTERNAL_LINKS_IN_BROWSER": False,
        "OPEN_DEVTOOLS_IN_DEBUG": userSettings["debug"],
    }
    while not cert_installed():
        subprocess.run(
            [
                "certutil.exe",
                "-user",
                "-addstore",
                "root",
                os.path.expanduser("~/.mitmproxy/mitmproxy-ca-cert.cer"),
            ]
        )

    def start():
        webview.start(debug=userSettings["debug"]) # have to make sure the loop isn't running when we block with the gui thread
        proxy_set(enabled=False)
    return start

def main():
    loop = asyncio.get_event_loop()
    threading.Thread(target=loop.run_forever, daemon=True).start()

    session = aiohttp.ClientSession(loop=loop)

    start = asyncio.run_coroutine_threadsafe(init(loop, session), loop).result()

    start()

    asyncio.run_coroutine_threadsafe(session.close(), loop).result() # close session

if __name__ == "__main__":
    main()
