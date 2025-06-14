import json
import os
import asyncio

import webbrowser
import aiohttp
from semver import Version
import webview

from multiprocessing.connection import Listener
from utils.mitmproxyserver import MitmproxyServer

import constants
import dll
import type_definitions

from api import checkDiscord
from api import getLatestVersion
from api import connect
from cosmetics import buildAthena
from addon import Addon

# Utils
from utils import discord
from utils import epicgames
from utils.epicgames import get_launcher_token
from utils.epicgames import get_exchange_code
from utils.epicgames import get_fortnite_pc_token
from utils.epicgames import get_common_core
from utils import config
from utils.misc import getVideo
from utils.misc import proxy_set
from utils.misc import sendXMPPMsg
from utils.misc import updateRPC

import modifications

from typing import Any, Callable, Coroutine, Concatenate

currentlyEquippedInternal: dict[str, str] = {
    "skin": "",
    "backpack": "",
    "glider": "",
    "contrail": "",
}


def addConsoleLog(level: str, msg: str):
    webview.windows[0].evaluate_js(f'addConsoleLog("{level}","{msg}")')


from utils import (
    console_logs as logger,
)  # to avoid circular reference, console_logs depends on addConsoleLog


def toggleStartButton(enabled: bool = True):
    if enabled:
        webview.windows[0].evaluate_js(f"setStartProxyButtonEnabled(true);")
    else:
        webview.windows[0].evaluate_js(f"setStartProxyButtonEnabled(false);")


def togglePremium(enabled: bool = True):
    if enabled:
        webview.windows[0].evaluate_js(f"setPremium(true);")
    else:
        webview.windows[0].evaluate_js(f"setPremium(false);")


def updateUsers(amount: int):
    webview.windows[0].evaluate_js(f"setUserCount({json.dumps(amount)})")


def updateCosmeticGraph(amount: int):
    webview.windows[0].evaluate_js(f"setCosmeticCount({json.dumps(amount)})")


def updateImage(
    userImageUrl: str = "https://fortnite-api.com/images/cosmetics/br/cid_001_athena_commando_f_default/icon.png",
):
    webview.windows[0].evaluate_js(f"setCosmeticImageURL({json.dumps(userImageUrl)})")


async def updateUserName(
    userSettings: type_definitions.defaultUserSettings, userName: str = "TBD"
):
    webview.windows[0].evaluate_js(f"setUsername(`{userName}`);")
    await updateRPC(userSettings, state=f"Logged in with {userName}")


def updateUserBadges(badges: list[type_definitions.Badge]):
    badgeStr: str = ""
    for badge in badges:
        if badge == badges[-1]:
            badgeStr += f"'{badge}'"
        else:
            badgeStr += f"'{badge}',"
    script: str = f"setBadges([{badgeStr}])"
    print(script)
    webview.windows[0].evaluate_js(script)


def sync_call[**P, R](func: Callable[Concatenate["Api", P], Coroutine[Any, Any, R]]):
    def wrapper(self: "Api", *args: P.args, **kwargs: P.kwargs) -> R:
        return asyncio.run_coroutine_threadsafe(
            func(self, *args, **kwargs), self.loop
        ).result()

    return wrapper


class Api:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        session: aiohttp.ClientSession,
        userSettings: type_definitions.defaultUserSettings,
    ):
        self.athena: dict[str, type_definitions.AthenaItem] = {}
        self.common_core: dict[str, type_definitions.AthenaItem] = {}
        self.userSettings = userSettings
        self.storedCosmetics: list[dict[str, str]] = []
        self.session = session
        self.addon = Addon(
            self.athena, self.userSettings, self.common_core, self.session
        )
        self.loop = loop

    @sync_call
    async def getUrl(self):
        code_verifier = discord.generate_code_verifier()
        print("Code", code_verifier)
        webbrowser.open_new_tab(
            discord.create_authorization_url(
                discord.generate_code_challenge(code_verifier)
            )
        )
        with Listener(constants.address, authkey=constants.authkey) as listener:
            with listener.accept() as conn:
                authCode = conn.recv()

        accessToken, refreshToken = await discord.exchange_for_tokens(
            self.session, code_verifier, authCode
        )

        config_data: type_definitions.Config = config.read()
        config_data["refreshToken"] = refreshToken

        with open(constants.configFilePath, "w") as f:
            json.dump(config_data, f, indent=2)
        await checkDiscord(self.session, accessToken, self.userSettings)
        webview.windows[0].evaluate_js("closeDiscordLogin()")
        updateUserBadges(self.userSettings["badges"])
        if self.userSettings["premium"]:
            togglePremium(enabled=True)

    def resetConfig(self):
        defaultConfig: type_definitions.Config = {
            "configVersion": constants.currentConfigVersion,
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
                "video": f"{constants.URLs.CDN}/maeko.mp4",
                "status": "👉 discord.gg/fortnitedev 🔌",
                "image": f"{constants.URLs.CDN}/SplashScreen.png",
                "radio_enabled": True,
                "nigga_enabled": True,
                "playlist": "playlist_nobuildbr_squads",
                "images_enabled": True,
                "replacements_enabled": True,
                "vbucks": 99999999999999999,
                "crowns": 69420,
                "display_name": "",
                "battlestars": 69420,
                "levels": 999,
            },
            "WebSocketLogging": False,
            "refreshToken": "",
            "tosAgreed": True,
        }

        with open(constants.configFilePath, "w") as f:
            json.dump(defaultConfig, f, indent=2)
            logger.info("Reset config_data!")
        os._exit(0)  # pyright: ignore[reportPrivateUsage]

    def giftAll(self):

        item: dict[str, type_definitions.AthenaItem] = {
            "BoogieGift_"
            + "EverySingleBombaclartItem": {
                "templateId": "GiftBox:GB_GiftWrap1",
                "attributes": {
                    "fromAccountId": "You",
                    "lootList": [
                        {
                            "itemProfile": "Athena",
                            "itemGuid": cosmetic["templateId"],
                            "itemType": cosmetic["templateId"],
                            "quantity": 1,
                        }
                        for cosmetic in self.athena.values()
                    ],
                    "level": 1,
                    "giftedOn": "2024-11-13T23:58:48.934Z",
                },
                "quantity": 1,
            }
        }

        self.common_core.update(item)
        self.athena.update(item)
        sendXMPPMsg(self.userSettings)
        self.addon.hasGift = True
        logger.fortnite(f"Gifted Every Item!")

    def gift(self, itemID: str):
        itemType: str = itemID.split("_")[0]
        backendType: str = constants.itemIDMap[itemType.upper()]

        itemTemplate = f"{backendType}:{itemID}"

        item: dict[str, type_definitions.AthenaItem] = {
            "BoogieGift_"
            + itemID: {
                "templateId": "GiftBox:GB_GiftWrap1",
                "attributes": {
                    "fromAccountId": "You",
                    "lootList": [
                        {
                            "itemType": itemTemplate,
                            "itemGuid": itemTemplate,
                            "itemProfile": "athena",
                            "quantity": 1,
                        }
                    ],
                    "level": 1,
                    "giftedOn": "2024-11-13T23:58:48.934Z",
                },
                "quantity": 1,
            }
        }

        self.common_core.update(item)
        self.athena.update(item)

        sendXMPPMsg(self.userSettings)
        self.addon.hasGift = True

        logger.fortnite(f"Gifted {itemID}!")

    def sendMessage(self, payload: str):
        print(payload)
        sendXMPPMsg(userSettings=self.userSettings, payload=payload)

    @sync_call
    async def getLatestVersion(self) -> str:
        version: Version = await getLatestVersion(self.session)
        return str(version)

    def invite(self) -> None:
        webbrowser.open_new_tab("https://discord.gg/fortnitedev")

    def isBanned(self) -> bool:
        return self.userSettings["banned"]

    def setCosmetics(
        self,
        skin: str | None,
        backpack: str | None,
        glider: str | None,
        contrail: str | None,
    ):

        if skin:
            currentlyEquippedInternal["skin"] = skin

        if backpack:
            currentlyEquippedInternal["backpack"] = backpack

        if glider:
            currentlyEquippedInternal["glider"] = glider

        if contrail:
            currentlyEquippedInternal["contrail"] = contrail

        message: dict[str, str] = {
            "action": "set_cosmetics",
            "skin": currentlyEquippedInternal["skin"],
            "backpack": currentlyEquippedInternal["backpack"],
            "glider": currentlyEquippedInternal["glider"],
            "contrail": currentlyEquippedInternal["contrail"],
        }

        dll.send(self.userSettings["pipe"], json.dumps(message))
        response: dict[str, str] = json.loads(dll.receive(self.userSettings["pipe"]))
        logger.info(response["log"])

    @sync_call
    async def checkPurchases(self) -> bool:
        if self.userSettings["debug"]:
            return False
        token: str = await get_launcher_token(self.session)
        self.userSettings["launcherToken"] = token
        exchangeCode: str = await get_exchange_code(self.session, token)
        pcToken, accountId = await get_fortnite_pc_token(self.session, exchangeCode)
        common_core: type_definitions.commonCoreFullProfile = await get_common_core(
            self.session, account_id=accountId, token=pcToken
        )
        return epicgames.checkCommonCore(common_core)

    def close(self):
        proxy_set(enabled=False)
        webview.windows[0].destroy()

    @sync_call
    async def startProxy(self):
        toggleStartButton(False)

        async def startProxy():
            mitmserver = MitmproxyServer(self.userSettings["debug"])
            mitmserver.m.addons.add(self.addon)
            modifications.add_addons(self.userSettings, mitmserver.m.addons)
            mitmserver.start()
            epicgames.closeFortnite()
            await asyncio.sleep(0.592)
            epicgames.startFortnite()
            pipe: int = dll.create_pipe()
            self.userSettings["pipe"] = pipe
            logger.info(f"Pipe to DLL Created: {pipe}")

        logger.info("Getting cosmetics!")
        await buildAthena(self.session, self.storedCosmetics, self.athena)
        await epicgames.changeEACImage(self.session)
        self.loop.create_task(startProxy())
        logger.info("Proxy Started!")
        self.loop.create_task(
            connect(
                self.session,
                {
                    "request": "connect",
                    "info": {"id": int(self.userSettings["discordAccountId"])},
                },
            )
        )

    def getSavedConfig(self):
        config_data: type_definitions.profileForm = config.read()["extraSettings"]
        self.userSettings["savedUrl"] = getVideo(config_data["video"])
        return config_data

    def getCosmetics(self):
        return self.storedCosmetics

    def shouldShowDiscordLogin(self) -> bool:
        if self.userSettings["discordAccountId"]:
            return False
        else:
            return True

    def restartProxy(self):
        pass  # TODO: add this

    def onConfigUpdate(self, conf: type_definitions.profileForm):
        config_data: type_definitions.Config = config.read()
        config_data["extraSettings"] = conf

        self.userSettings["savedUrl"] = getVideo(conf["video"])

        with open(constants.configFilePath, "w") as f:
            json.dump(config_data, f, indent=2)

    def getVersion(self):
        return str(constants.version)

    def update(self):
        webbrowser.open_new_tab(f"https://api.teamboogie.lol/download")
        os._exit(0)  # type: ignore # stfu
