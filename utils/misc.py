import type_definitions
import constants
import json
import yt_dlp
import typing
import asyncio
import winreg
import xml.etree.ElementTree as ET
import uuid

from datetime import datetime

from mitmproxy import ctx
from mitmproxy.http import HTTPFlow

from pypresence import AioPresence

from .epicgames import getFortniteVersion
from .epicgames import getUserAgents

if constants.isRPC:
    try:
        RPC = AioPresence(client_id=constants.client_id)
    except:
        pass

async def connectRPC():
    if constants.isRPC:
        await RPC.connect()

def is_fortnite_user_agent(user_agent: str):
    game_version = getFortniteVersion()
    user_agents = getUserAgents(game_version)
    split_user_agent = user_agent.split(sep="/")

    if len(split_user_agent) >= 2:
        corrected_user_agent = split_user_agent[1].replace(" ", "-")
    else:
        corrected_user_agent = user_agent

    return corrected_user_agent in user_agents


def getVideo(videoUrl: str):
    if videoUrl.endswith(".mp4"):
        return videoUrl
    with yt_dlp.YoutubeDL(
        {
            "format": "[acodec!=none]",
            "quiet": True,
            "compat_opts": ["no-certifi"],
        }
    ) as ydl:
        try:
            info = ydl.extract_info(videoUrl, download=False)  # not my fault
        except yt_dlp.utils.DownloadError:
            return None
        assert info is not None
        return typing.cast(str, info["url"])


def proxy_set(enabled: bool = True):
    INTERNET_SETTINGS = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings",
        0,
        winreg.KEY_WRITE,
    )
    winreg.SetValueEx(
        INTERNET_SETTINGS, "ProxyServer", 0, winreg.REG_SZ, "127.0.0.1:1942"
    )
    winreg.SetValueEx(
        INTERNET_SETTINGS, "ProxyEnable", 0, winreg.REG_DWORD, int(enabled)
    )


def sendXMPPMsg(
    userSettings: type_definitions.defaultUserSettings,
    msg: type_definitions.XMPPMessage | None = None,
    payload: str | None = None,
):
    xmppFlow: HTTPFlow | None = userSettings["xmppFlow"]
    if msg is None and payload:
        msg = {
            "sent": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "type": constants.XMPPMessageType.GiftReceived,
            "payload": "",
        }
    body: str = json.dumps(msg)

    if payload:  # if full custom msg
        sent: str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        body = payload
        body = body.replace("{sent}", sent)

    message = ET.Element(
        "message",
        {
            "xmlns": "jabber:client",
            "to": f"{userSettings['accountId']}@prod.ol.epicgames.com/{userSettings['jid']}",
            "id": str(uuid.uuid4()),
            "from": "xmpp-admin@prod.ol.epicgames.com",
        },
    )
    print(f"{userSettings['accountId']}@prod.ol.epicgames.com/{userSettings['jid']}")
    body_elem = ET.SubElement(message, "body")
    body_elem.text = body
    resp: bytes = ET.tostring(message)

    async def inject():
        ctx.master.commands.call("inject.websocket", xmppFlow, True, resp)

    asyncio.run(inject())


async def updateRPC(
    userSettings: type_definitions.defaultUserSettings, state: str | None = None
):
    if userSettings["premium"] == True:
        small_text: str = "Boogie+ User"
        small_image = f"{constants.URLs.CDN}/newprem.png"
    else:
        small_text: str = "Boogie Basic User"
        small_image: str = f"{constants.URLs.CDN}/bomb.png?size=small"

    if constants.isRPC:
        await RPC.update(  # not my fault
            state=typing.cast(str, state),
            buttons=[
                {
                    "label": "Boogie",
                    "url": "https://discord.gg/fortnitedev",
                },
                {
                    "label": "Boogie+",
                    "url": "https://boogiexshop.mysellix.io/",
                },
            ],
            large_image=f"{constants.URLs.CDN}/bomb.png?size=small",
            large_text=constants.title,
            small_image=small_image,
            small_text=small_text,
        )
    return
