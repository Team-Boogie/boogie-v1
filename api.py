import constants
import type_definitions

# from websockets.sync import client
# import websockets
import aiohttp
import semver
from utils import discord

WEBSOCKET_URL: str = f"{constants.URLs.COMMANDO.replace("http","ws",1)}/join" # http:// to ws:// and https:// to wss://


async def get_profile(session: aiohttp.ClientSession, id: str) -> type_definitions.ProfileInfo:
    async with session.get(f"{constants.URLs.API}/profile/{id}") as resp:
        return await resp.json()

async def connect(session: aiohttp.ClientSession, info: type_definitions.WebsocketInitialMessage):  # {"request": "connect", "info": {"id": asd}}
    async with session.ws_connect(WEBSOCKET_URL) as websocket:
        await websocket.send_json(info)
        while command := await websocket.receive_json():
            
            if not command.get("command"):  
                continue
            
            if command["command"] == "disconnect":
                await websocket.close()
            await websocket.send_json({"response": "ok!"})


async def getLatestVersion(session: aiohttp.ClientSession):
    async with session.get(f"{constants.URLs.API}/latest") as resp:
        return semver.Version.parse(await resp.text())


async def checkDiscord(session: aiohttp.ClientSession, access_token: str, userSettings: type_definitions.defaultUserSettings):
    accountId = await discord.get_id(session, access_token)
    data = await get_profile(session, accountId)

    userSettings["discordAccountId"] = accountId

    if data.get("banned"):
        if data.get("banned") == True:
            userSettings["banned"] = data.get("banned")

    if data.get("member"):
        if data.get("member") == True:
            userSettings["member"] = data.get("member")

    if data.get("premium"):
        if data.get("premium") == True:
            userSettings["premium"] = data.get("premium")

    if data.get("badges"):
        recievedbadges = data.get("badges")
        if recievedbadges:
            userSettings["badges"] = recievedbadges
