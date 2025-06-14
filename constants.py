import semver
import os

from enum import StrEnum
from pypresence.utils import get_ipc_path  # not my fault

version: semver.Version = semver.Version.parse("1.2.1")

CLIENT_ID = "1289319139550433420"
CLIENT_SECRET = "nuh uh"


class XMPPMessageType(StrEnum):
    GiftReceived = "com.epicgames.gift.received"


class URLs(StrEnum):
    API = "https://api.teamboogie.lol"
    # API = "http://localhost:8787"
    CDN = "https://cdn.teamboogie.lol"
    COMMANDO = "https://commando.pirxcy.dev"


isRPC = bool(get_ipc_path())
title: str = f"Boogie - {version}"
currentConfigVersion: float = 1.2
configDir: str = os.path.join(os.environ["localappdata"], "Programs", "Boogie")
configFilePath: str = os.path.join(
    os.environ["localappdata"], "Programs", "Boogie", "config.json"
)

game_user_settings_path: str = os.path.join(
    os.environ["localappdata"],
    "EpicGamesLauncher",
    "Saved",
    "Config",
    "Windows",
    "GameUserSettings.ini",
)

address = ("localhost", 6000)
authkey = b"boogie ipc stuff password wow"

client_id = "1289319139550433420"

closeTasks: list[str] = [
    "taskkill /f /im epicgameslauncher.exe > nul",
    "taskkill /f /im FortniteClient-Win64-Shipping_EAC.exe > nul",
    "taskkill /f /im FortniteClient-Win64-Shipping_BE.exe > nul",
    "taskkill /f /im FortniteLauncher.exe > nul",
    "taskkill /f /im FortniteClient-Win64-Shipping.exe > nul",
    "taskkill /f /im EpicGamesLauncher.exe > nul",
    "taskkill /f /im UnrealCEFSubProcess.exe > nul",
    "taskkill /f /im EasyAntiCheat.exe > nul",
    "taskkill /f /im BEService.exe > nul",
    "taskkill /f /im BEServices.exe > nul",
    "taskkill /f /im BattleEye.exe > nul",
    "taskkill /f /im FortniteClient-Win64-Shipping_EAC.exe > nul",
    "taskkill /f /im FortniteClient-Win64-Shipping_BE.exe > nul",
    "taskkill /f /im FortniteLauncher.exe > nul",
    "taskkill /f /im OneDrive.exe > nul",
    "taskkill /f /im FortniteClient-Win64-Shipping.exe > nul",
    "taskkill /f /im EpicGamesLauncher.exe > nul",
    "taskkill /f /im UnrealCEFSubProcess.exe > nul",
    "taskkill /f /im CEFProcess.exe > nul",
    "taskkill /f /im EasyAntiCheat.exe > nul",
    "taskkill /f /im BEService.exe > nul",
    "taskkill /f /im BEServices.exe > nul",
    "taskkill /f /im BattleEye.exe > nul",
    "Sc stop FortniteClient-Win64-Shipping_EAC",
    "Sc stop FortniteClient-Win64-Shipping_BE",
    f'del /f /s /q {os.environ.get("systemdrive")}\\Program Files\\Epic Games\\Fortnite\\FortniteGame\\PersistentDownloadDir\\*.*"',
]


itemIDMap: dict[str, str] = {
    "CID": "AthenaCharacter",
    "BID": "AthenaBackpack",
    "EID": "AthenaDance",
    "PICKAXE": "AthenaPickaxe",
    "CHARACTER": "AthenaCharacter",
    "BACKPACK": "AthenaBackpack",
}

itemTypeMap: dict[str, str] = {
    "emote": "AthenaDance",
    "backpack": "AthenaBackpack",
    "pet": "AthenaBackpack",
    "outfit": "AthenaCharacter",
    "toy": "AthenaDance",
    "glider": "AthenaGlider",
    "emoji": "AthenaDance",
    "spray": "AthenaDance",
    "music": "AthenaMusicPack",
    "bannertoken": "HomebaseBannerIcon",
    "contrail": "AthenaSkyDiveContrail",
    "wrap": "AthenaItemWrap",
    "loadingscreen": "AthenaLoadingScreen",
    "pickaxe": "AthenaPickaxe",
    "vehicle_wheel": "VehicleCosmetics_Wheel",
    "vehicle_wheel": "VehicleCosmetics_Wheel",
    "vehicle_skin": "VehicleCosmetics_Skin",
    "vehicle_booster": "VehicleCosmetics_Booster",
    "vehicle_body": "VehicleCosmetics_Body",
    "vehicle_drifttrail": "VehicleCosmetics_DrifTrail",
    "vehicle_cosmeticvariant": "CosmeticVariantToken",
    "cosmeticvariant": "none",
    "bundle": "AthenaBundle",
    "battlebus": "AthenaBattleBus",
    "itemaccess": "none",
    "sparks_microphone": "SparksMicrophone",
    "sparks_keyboard": "SparksKeyboard",
    "sparks_bass": "SparksBass",
    "sparks_drum": "SparksDrums",
    "sparks_guitar": "SparksGuitar",
    "sparks_aura": "SparksAura",
    "sparks_song": "SparksSong",
    "building_set": "JunoBuildingSet",
    "building_prop": "JunoBuildingProp",
    "shoes": "CosmeticShoes",
}

dash_api_map = {
    "AthenaEmoji": "AthenaDance",
    "AthenaSpray": "AthenaDance",
    "AthenaToy": "AthenaDance",
    "AthenaPetCarrier": "AthenaBackpack",
    "AthenaPet": "AthenaBackpack",
    "SparksDrum": "SparksDrums",
    "SparksMic": "SparksMicrophone",
}

backendTypeMap: dict[str, str] = {"CID": "AthenaCharacter"}
