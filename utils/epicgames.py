import base64
import os
import json

import aiohttp

import type_definitions
import psutil
import time  # pyright: ignore[reportShadowedImports] # idfk man
from . import console_logs as logger
from . import translation
import constants
import configparser
from legendary.utils.egl_crypt import decrypt_epic_data  # not my fault
from legendary.api.lgd import LGDAPI


def getLauncherInstalled():
    programDataPath = os.getenv(key="ProgramData")
    assert programDataPath is not None
    path: str = os.path.join(
        programDataPath, "Epic", "UnrealEngineLauncher", "LauncherInstalled.dat"
    )

    with open(file=path) as file:
        launcherInstalled: type_definitions.LauncherInstalled = json.load(file)

    return launcherInstalled


def getUserAgents(gameVersion: str):
    userAgents: list[str] = ["X-UnrealEngine-Agent", gameVersion]
    return userAgents


def getGameInfo(gameName: str):
    Installed: type_definitions.LauncherInstalled = getLauncherInstalled()

    for InstalledGame in Installed["InstallationList"]:
        if InstalledGame["AppName"].upper() == gameName.upper():
            info: type_definitions.GameInfo = {
                "path": InstalledGame["InstallLocation"],
                "version": InstalledGame["AppVersion"],
                "name": InstalledGame["AppName"],
                "id": InstalledGame["ItemId"],
            }

            return info

    return None


def isLaunched(processName: str = "FortniteClient-Win64-Shipping.exe") -> bool:

    processes: list[str] = [i.info["name"] for i in psutil.process_iter(["name"])]

    if processName in processes:
        launched = True
    else:
        launched = False

    return launched


def checkForKill(processName: str = "FortniteClient-Win64-Shipping.exe"):
    killed = False

    while not killed:
        processes = [i.info["name"] for i in psutil.process_iter(["name"])]

        if processName not in processes:

            killed = True
            break

        else:
            time.sleep(1)

    return killed


def getFortniteVersion() -> str:
    info: type_definitions.GameInfo | None = getGameInfo(gameName="FORTNITE")
    assert info is not None
    version: str = info["version"]
    return version


def closeFortnite():
    jointCommand: str = ""
    for command in constants.closeTasks:
        jointCommand += command + " & "

    os.system(jointCommand)


def startFortnite():
    os.system(
        "start com.epicgames.launcher://apps/fn%3A4fe75bbc5a674f4f9b356b5c90567da5%3AFortnite?action=launch"
    )
    logger.fortnite(translation.get("console-starting-fortnite"))


async def changeEACImage(session: aiohttp.ClientSession):
    program_data = os.getenv("ProgramData")

    assert program_data is not None

    path: str = os.path.join(
        program_data, "Epic", "UnrealEngineLauncher", "LauncherInstalled.dat"
    )
    with open(path) as file:
        Installed: type_definitions.LauncherInstalled = json.load(file)

    EasyAntiCheatLocation = next(
        os.path.join(
            InstalledGame["InstallLocation"].replace("/", "\\"),
            "FortniteGame",
            "Binaries",
            "Win64",
            "EasyAntiCheat",
        ).replace("/", "\\")
        for InstalledGame in Installed["InstallationList"]
        if InstalledGame["AppName"].upper() == "FORTNITE"
    )  # not as readable as i'd like but python doesn't have an array find function so yeah

    with open(EasyAntiCheatLocation + "\\" + "SplashScreen.png", "wb") as dest_file:
        async with session.get(f"{constants.URLs.CDN}/EAC.png") as resp:
            async for chunk in resp.content.iter_chunked(128):
                dest_file.write(chunk)

    logger.info(translation.get("console-update-eac-image"))


def get_remember_me_data() -> type_definitions.RememberMe:
    game_user_settings = configparser.ConfigParser(strict=False)
    game_user_settings.read(constants.game_user_settings_path, encoding="utf-8")

    remember_me_data = game_user_settings.get("RememberMe", "Data")

    raw_data = base64.b64decode(remember_me_data)

    try:
        re_data = json.loads(raw_data)
    except UnicodeDecodeError:
        version_info = LGDAPI().get_version_information()

        data_key = version_info["egl_config"]["data_keys"][0]

        decrypted_data = decrypt_epic_data(data_key, raw_data)  # utf-8
        re_data = json.loads(decrypted_data)

    return re_data[0]


def set_remember_me_data(data: type_definitions.RememberMe):
    game_user_settings = configparser.ConfigParser(strict=False)
    game_user_settings.read(constants.game_user_settings_path)

    decrypted_data = json.dumps([data])

    game_user_settings.set(
        "RememberMe", "Data", base64.b64encode(decrypted_data.encode()).decode()
    )

    with open(constants.game_user_settings_path, "w") as game_user_settings_file:
        game_user_settings.write(game_user_settings_file)


async def get_launcher_token(session: aiohttp.ClientSession) -> str:
    remember_me_data = get_remember_me_data()
    refresh_token = remember_me_data["Token"]

    async with session.post(
        "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
        auth=aiohttp.BasicAuth(
            "34a02cf8f4414e29b15921876da36f9a", "daafbccc737745039dffe53d94fc76cf"
        ),
        data={"grant_type": "refresh_token", "refresh_token": refresh_token},
    ) as resp:
        data = await resp.json()

    remember_me_data["Token"] = data["refresh_token"]
    set_remember_me_data(remember_me_data)

    return data["access_token"]


async def get_exchange_code(session: aiohttp.ClientSession, token: str) -> str:
    async with session.get(
        "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange",
        headers={"Authorization": f"bearer {token}"},
    ) as resp:
        return (await resp.json())["code"]


async def get_fortnite_pc_token(
    session: aiohttp.ClientSession, exchange_code: str
) -> tuple[str, str]:
    async with session.post(
        "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
        auth=aiohttp.BasicAuth(
            "ec684b8c687f479fadea3cb2ad83f5c6", "e1f31c211f28413186262d37a13fc84d"
        ),
        data={"grant_type": "exchange_code", "exchange_code": exchange_code},
    ) as resp:
        data = await resp.json()

    return data["access_token"], data["account_id"]


async def get_common_core(
    session: aiohttp.ClientSession, account_id: str, token: str
) -> type_definitions.commonCoreFullProfile:
    async with session.post(
        f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile",
        headers={"Authorization": f"bearer {token}"},
        json={},
    ) as resp:
        return await resp.json()


def checkCommonCore(data: type_definitions.commonCoreFullProfile) -> bool:
    return bool(data["profileChanges"][0]["profile"]["stats"][
        "attributes"
    ]["in_app_purchases"]["fulfillmentCounts"])