from configparser import ConfigParser
from io import StringIO
import json
import re
from typing import NotRequired, TypedDict

from mitmproxy import http

from type_definitions import defaultUserSettings
from type_definitions import CloudstorageSystemConfig
from utils import checks
from utils import console_logs as logger
from utils import translation
import hashlib

from utils import config


def system_config(config: CloudstorageSystemConfig):  # for type validation
    return config


class TextReplacement(TypedDict):
    category: NotRequired[str]
    is_minimal_patch: NotRequired[bool]
    namespace: str
    key: str
    native_string: str
    localized_strings: dict[str, str]


class Patch(TypedDict):
    scripts: dict[str, dict[str, str]]
    text_replacements: NotRequired[list[TextReplacement]]


class dqstr(str):
    def __repr__(self):
        return json.dumps(self)


def write_string(config: ConfigParser):
    io = StringIO()
    config.write(io)
    data = io.getvalue()
    io.close()
    return data


LANGUAGES = [
    "ar",  # Arabic
    "en",  # English
    "de",  # German
    "es",  # Spanish
    "es_419",  # Latin American Spanish
    "fr",  # French
    "it",  # Italian
    "ja",  # Japanese
    "ko",  # Korean
    "pl",  # Polish
    "pt_BR",  # Portuguese
    "ru",  # Russian
    "tr",  # Turkish
    "zh_CN",  # Simplified Chinese
    "zh_Hant",  # Traditional Chinese
]


def encode_patch(patch: Patch):
    config = ConfigParser()
    config.optionxform = lambda optionstr: optionstr # case sensitive

    for script in patch["scripts"]:
        config[script] = patch["scripts"][script]

    if "text_replacements" in patch:
        config["/Script/FortniteGame.FortTextHotfixConfig"] = {}

    data = write_string(config)

    if "text_replacements" in patch:
        for text_replacement in patch["text_replacements"]:
            filled_localized_strings = {
                key: val for key, val in text_replacement["localized_strings"].items()
            }
            for lang in LANGUAGES:
                filled_localized_strings[lang] = (
                    filled_localized_strings.get(lang)
                    or filled_localized_strings.get("en")
                    or ""
                )
            localized_strings = repr(
                tuple(
                    (dqstr(key), dqstr(val))
                    for key, val in filled_localized_strings.items()
                )
            )

            data += f"+TextReplacements=(Category={json.dumps(text_replacement.get("category", "Game"))}, bIsMinimalPatch={text_replacement.get("is_minimal_patch", True)}, Namespace={json.dumps(text_replacement["namespace"])}, Key={json.dumps(text_replacement["key"])}, NativeString={json.dumps(text_replacement["native_string"])}, LocalizedStrings={localized_strings})\n"

    return data


def sha1(msg: str) -> str:
    return hashlib.sha1(msg.encode()).hexdigest()


def sha256(msg: str) -> str:
    return hashlib.sha256(msg.encode()).hexdigest()


class CloudStorage:
    def __init__(self, userSettings: defaultUserSettings):
        self.userSettings: defaultUserSettings = userSettings

    @checks.is_fortnite_request
    def request(self, flow: http.HTTPFlow):
        headers = ()
        match (
            match := re.match(
                r"^https:\/\/fngw-mcp-gc-livefn\.ol\.epicgames\.com\/fortnite\/api\/cloudstorage\/system(.*)$",
                flow.request.url,
            )
        ) and match.groups()[0]:
            case None:
                return
            case "/config":
                content = self.system_config
                headers = http.Headers(content_type="application/json")
            case "/DefaultEngine.ini":
                content = self.default_engine
                logger.fortnite(
                    translation.get("console-cs-file").format("DefaultEngine.ini")
                )
            case "/DefaultGame.ini":
                content = self.default_game
                logger.fortnite(
                    translation.get("console-cs-file").format("DefaultGame.ini")
                )
            case "/DefaultRuntimeOptions.ini":
                content = self.default_runtime_options
                logger.fortnite(
                    translation.get("console-cs-file").format(
                        "DefaultRuntimeOptions.ini"
                    )
                )
            case "":
                content = self.system_files
                headers = http.Headers(content_type="application/json")
            case _:
                return

        flow.response = http.Response.make(200, content, headers)

    system_config = json.dumps(
        system_config(
            {
                "lastUpdated": "2027-01-24T12:29:55.851Z",
                "disableV2": False,
                "isAuthenticated": False,
                "enumerateFilesPath": "/api/cloudstorage/system",
                "enableMigration": False,
                "enableWrites": False,
                "epicAppName": "Live",
                "transports": {
                    "McpProxyTransport": {
                        "name": "McpProxyTransport",
                        "type": "ProxyStreamingFile",
                        "appName": "fortnite",
                        "isEnabled": True,
                        "isRequired": True,
                        "isPrimary": True,
                        "timeoutSeconds": 30,
                        "priority": 10,
                    },
                    "McpSignatoryTransport": {
                        "name": "McpSignatoryTransport",
                        "type": "ProxySignatory",
                        "appName": "fortnite",
                        "isEnabled": False,
                        "isRequired": False,
                        "isPrimary": False,
                        "timeoutSeconds": 30,
                        "priority": 20,
                    },
                    "DssDirectTransport": {
                        "name": "DssDirectTransport",
                        "type": "DirectDss",
                        "appName": "fortnite",
                        "isEnabled": True,
                        "isRequired": False,
                        "isPrimary": False,
                        "timeoutSeconds": 30,
                        "priority": 30,
                    },
                },
            }
        )
    )

    default_engine = encode_patch(
        {
            "scripts": {
                "/Script/Engine.PlayerInput": {
                    "bEnableMouseSmoothing": "false",
                    "ConsoleKeys": "(Key=F1)",
                },
                "Core.Log": {
                    "LogEngine": "All",
                    "LogNetDormancy": "All",
                    "LogNetPartialBunch": "All",
                    "OodleHandlerComponentLog": "All",
                    "LogSpectatorBeacon": "All",
                    "LogHttp": "All",
                    "LogProfileSys": "All",
                    "LogOnlineAccount": "All",
                    "LogOnline": "All",
                    "LogOnlineInteractions": "All",
                    "LogAnalytics": "All",
                    "PacketHandlerLog": "All",
                    "LogPartyBeacon": "All",
                    "LogNet": "All",
                    "LogBeacon": "All",
                    "LogNetTraffic": "All",
                    "LogDiscordRPC": "All",
                    "LogEOSSDK": "All",
                    "LogXmpp": "All",
                    "LogParty": "All",
                    "LogHotfixManager": "All",
                    "LogMatchmakingServiceClient": "All",
                    "LogScriptCore": "All",
                    "LogSkinnedMeshComp": "All",
                    "LogFortAbility": "All",
                    "LogContentBeacon": "All",
                    "LogEasyAntiCheatServer": "All",
                    "LogEasyAntiCheatClient": "All",
                    "LogBattlEye": "All",
                },
            }
        }
    )

    @property
    def default_game(self):
        patch: Patch = {
            "scripts": {
                "/Script/Account.OnlineAccountCommon": {
                    "bEnableWaitingRoom": "false",
                    "bShouldGrantFreeAccess": "true",
                    "bRequireUGCPrivilege": "false",
                    "bAllowLocalLogout": "true",
                    "SkipRedeemOfflinePurchasesChance": "true",
                    "bAllowHomeSharingAccess": "true",
                    "bEnableDevLoginStepTimeouts": "true",
                    "bRequireLightswitchAtStartup": "false",
                },
                "/Script/FortniteGame.FortAnalyticsConfig": {
                    "UrlEndpoint": '""',
                    "AltDomains": "Clear",
                },
                "/Script/FortniteGame.FortOnlineAccount": {
                    "b50v50ForceEnabled": "true",
                    "bPlatoonForceEnabled": "true",
                    "bShootingTest3Enabled": "true",
                    "bEvent1ForceEnabled": "true",
                    "bEvent2ForceEnabled": "true",
                    "bEvent3ForceEnabled": "true",
                    "bEvent4ForceEnabled": "true",
                    "bEvent5ForceEnabled": "true",
                    "bEvent6ForceEnabled": "true",
                    "bEvent7ForceEnabled": "true",
                    "bEvent8ForceEnabled": "true",
                    "bEnableWIFE": "true",
                    "bEnableCreativeModeLimitedAccess": "true",
                    "bShowExtendedBattlePassMovie": "false",
                    "MaxElectraFpsVideos": "240",
                    "bPapayaSpeakersEnabled": "true",
                    "bGlobalLeaderboardsFrontEndEnabled": "false",
                    "bUploadAthenaStatsV2": "false",
                    "bAthenaStatsFrontendEnabled": "false",
                    "bAllowLogout": "true",
                    "bAllowQuit": "true",
                    "bEnableCreativeModeTutorials": "true",
                    "bEnableCreativeMode": "true",
                    "bEnableFriendCodes": "true",
                    "bEnablePlayerTriggeredRespawn": "true",
                    "bEnableAIDespawning": "true",
                    "bEnableHestia": "true",
                    "bEnableWargameDebug": "true",
                    "bEnableEnduranceDebug": "true",
                },
                "/Script/FortniteGame.FortGlobals": {
                    "bEnableEula": "true",
                    "bHadLoginPurchaseCheckFailure": "false",
                    "bShouldCallPurchaseRedemptionOnApplicationReactivate": "false",
                    "bMergePerPlayerEncryptionKeysOnLogin": "false",
                },
            }
        }

        if (
            not self.userSettings["premium"]
            or config.read()["extraSettings"]["replacements_enabled"]
        ):
            patch["scripts"]["/Script/FortniteGame.FortOnlineAccount"] = {
                "bEnableEulaCheck": "false",
                "bHadLoginPurchaseCheckFailure": "false",
                "bShouldCallPurchaseRedemptionOnApplicationReactivate": "false",
                "bMergePerPlayerEncryptionKeysOnLogin": "false",
            }

            patch["text_replacements"] = [
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_SaltySprings",
                    "native_string": "SALTY SPRINGS",
                    "localized_strings": {"en": "SIZZY'S ENDS"},
                },
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_DirtyDocks",
                    "native_string": "DIRTY DOCKS",
                    "localized_strings": {"en": "THIRTY COCKS 🍆"},
                },
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_FrenzyFarm",
                    "native_string": "FRENZY FARM",
                    "localized_strings": {"en": "FINGER FUCK FARM"},
                },
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_PleasantPark",
                    "native_string": "PLEASANT PARK",
                    "localized_strings": {"en": "PIRXCY'S PARK"},
                },
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_PowerPlant",
                    "native_string": "STEAMY STACKS",
                    "localized_strings": {"en": "STEAMY VAPE LOUNGE"},
                },
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_MountainMeadow",
                    "native_string": "MISTY MEADOWS",
                    "localized_strings": {"en": "MYLO'S MEADOWS"},
                },
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_SlurpySwamp",
                    "native_string": "SLURPY SWAMP",
                    "localized_strings": {"en": "LIQUID LULU'S"},
                },
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_BeachyBluffs",
                    "native_string": "CRAGGY CLIFFS",
                    "localized_strings": {"en": "CAPS'S CLIFFS"},
                },
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_TheRig",
                    "native_string": "THE RIG",
                    "localized_strings": {"en": "NEVALEAH'S RIG"},
                },
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_Yacht",
                    "native_string": "THE YACHT",
                    "localized_strings": {"en": "KIKO'S DROP"},
                },
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_LemonCart",
                    "native_string": "THE DOGGPOUND",
                    "localized_strings": {"en": "PIXLD'S POUND"},
                },
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_LazyLake",
                    "native_string": "LAZY LAKE",
                    "localized_strings": {"en": "NEVA'S DROP"},
                },
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_HollyHedges",
                    "native_string": "HOLLY HEDGES",
                    "localized_strings": {"en": "HOLY SHIT"},
                },
                {
                    "namespace": "DisplayNamesForPOIs_Apollo_Terrain_Retro",
                    "key": "NameForLocation_Athena_Location_POI_WeepingWoods",
                    "native_string": "WEEPING WOODS",
                    "localized_strings": {"en": "KAZ'S HOME"},
                },
                {
                    "namespace": "",
                    "key": "C4CD7B84455129682D85E6B942CEF945",
                    "native_string": "locker",
                    "localized_strings": {"en": "LOCKER (Boogie)"},
                },
                {
                    "namespace": "",
                    "key": "CB51EA2B48FC45F33DD1D883CB2E345D",
                    "native_string": "locker",
                    "localized_strings": {"en": "LOCKER (Boogie)"},
                },
                {
                    "namespace": "",
                    "key": "74641AF241CABACB41136D9052C91BBC",
                    "native_string": "LOCKER",
                    "localized_strings": {"en": "LOCKER (Boogie)"},
                },
                {
                    "namespace": "",
                    "key": "74641AF241CABACB41136D9052C91BBC",
                    "native_string": "LOCKER",
                    "localized_strings": {"en": "LOCKER (Boogie)"},
                },
                {
                    "namespace": "",
                    "key": "03875FFD49212D2F37B01788C09086B5",
                    "native_string": "Quit",
                    "localized_strings": {"en": "QUIT Boogie?"},
                },
                {
                    "namespace": "",
                    "key": "1D20854C403FDD474AE7C8B929815DA2",
                    "native_string": "Quit",
                    "localized_strings": {"en": "QUIT Boogie?"},
                },
                {
                    "namespace": "",
                    "key": "2E42C9FB4F551A859C05BF99F7E36FB1",
                    "native_string": "Quit",
                    "localized_strings": {"en": "QUIT Boogie?"},
                },
                {
                    "namespace": "",
                    "key": "370415344EEEA09D8C01A48F4B8148D7",
                    "native_string": "Quit",
                    "localized_strings": {"en": "QUIT Boogie?"},
                },
                {
                    "namespace": "",
                    "key": "538BD1FD46BCEFA4813E2FAFAA07E1A2",
                    "native_string": "Quit",
                    "localized_strings": {"en": "QUIT Boogie?"},
                },
                {
                    "namespace": "MMRegion",
                    "key": "AutoRegion",
                    "native_string": "Auto",
                    "localized_strings": {"en": "🚀"},
                },
                {
                    "namespace": "MMRegion",
                    "key": "Europe",
                    "native_string": "Europe",
                    "localized_strings": {"en": "pirxcy's area 👍"},
                },
                {
                    "namespace": "Athena",
                    "key": "AnonymousMode_Anonymous",
                    "native_string": "Anonymous",
                    "localized_strings": {"en": "discord.gg/fortnitedev - "},
                },
                {
                    "namespace": "Athena",
                    "key": "RebootedPlayerName",
                    "native_string": "<{VictimStyle}>{PlayerName}</> was rebooted",
                    "localized_strings": {
                        "en": "fuck sake <{VictimStyle}>{PlayerName}</> just got rebooted."
                    },
                },
                {
                    "namespace": "Athena",
                    "key": "ThankedBusDriverCustom",
                    "native_string": "<{VictimStyle}>{PlayerName}</> {BusDriverMessage}",
                    "localized_strings": {
                        "en": "<{VictimStyle}>{PlayerName}</> is a bitch nigga. (i hope they die)"
                    },
                },
                {
                    "namespace": "Athena",
                    "key": "ThankedBusDriver",
                    "native_string": "<{VictimStyle}>{PlayerName}</> has thanked the bus driver",
                    "localized_strings": {
                        "en": "<{VictimStyle}>{PlayerName}</> is a bitch nigga. (i hope they die)"
                    },
                },
                {
                    "namespace": "BuildingActorGameplaySpawnChip",
                    "key": "RebootChipFDetailsormatText",
                    "native_string": "{0}'s Reboot Card",
                    "localized_strings": {
                        "en": "{0}'s Reboot Card (how tf did this nigga die)"
                    },
                },
                {
                    "namespace": "FortUINotificationManager",
                    "key": "PartyInviteDetailsSent",
                    "native_string": "Party invite sent to <Username>{0}</>",
                    "localized_strings": {
                        "en": "lets hope <Username>{0}</> fucking accepts!"
                    },
                },
                {
                    "namespace": "NetworkErrors",
                    "key": "McpErrorFmt",
                    "native_string": "Ack! We got disconnected from Fortnite. Sorry about that. Make sure your internet connection is still good and try again. If it keeps up, visit {CheckStatusURL}.\n\n{ErrorMessage}",
                    "localized_strings": {"en": "Ignore This Error! (Boogie)"},
                },
                {
                    "namespace": "NetworkErrors",
                    "key": "McpErrorFmt",
                    "native_string": "Ack! We got disconnected from the match. Sorry about that. Make sure your internet connection is still good and try again. If it keeps up, visit {CheckStatusURL}.",
                    "localized_strings": {"en": "Ignore This Error! (Boogie)"},
                },
                {
                    "namespace": "NetworkErrors",
                    "key": "ReturnToMainMenuDisconnect",
                    "native_string": "Ack! We got disconnected from the match. Sorry about that. Make sure your internet connection is still good and try again. If it keeps up, visit {CheckStatusURL}.",
                    "localized_strings": {"en": "Ignore This Error! (Boogie)"},
                },
                {
                    "namespace": "NetworkErrors",
                    "key": "PartyKickPlayerCheatingPlatform",
                    "native_string": "You were removed from the match due to internet lag, your IP or machine, VPN usage, for cheating, or being on an untrusted platform. We recommend not utilizing VPN or proxy services while attempting to play Fortnite.",
                    "localized_strings": {
                        "en": "In-Game Method in #faq\ndiscord.gg/fortnitedev"
                    },
                },
                {
                    "namespace": "NetworkErrors",
                    "key": "PartyKickPlayerCheating",
                    "native_string": "You were removed from the match due to internet lag, your IP or machine, VPN usage, for cheating, or being on an untrusted platform. We recommend not utilizing VPN or proxy services while attempting to play Fortnite.",
                    "localized_strings": {
                        "en": "In-Game Method in #faq\ndiscord.gg/fortnitedev"
                    },
                },
                {
                    "namespace": "Fortnite.FortAthenaMatchmakingWidget",
                    "key": "Message.CheckingForUpdates",
                    "native_string": "Checking for Updates...",
                    "localized_strings": {"en": "discord.gg/fortnitedev"},
                },
                {
                    "namespace": "Fortnite.FortAthenaMatchmakingWidget",
                    "key": "Message.WaitingForMatchmakingStart",
                    "native_string": "Waiting for matchmaking to commence...",
                    "localized_strings": {"en": "discord.gg/fortnitedev"},
                },
                {
                    "namespace": "Fortnite.FortAthenaMatchmakingWidget",
                    "key": "Message.QueueFull",
                    "native_string": "Queue is full, please wait...\nElapsed: {0}",
                    "localized_strings": {"en": "discord.gg/fortnitedev"},
                },
                {
                    "namespace": "Fortnite.FortAthenaMatchmakingWidget",
                    "key": "PublicMatch",
                    "native_string": "Public",
                    "localized_strings": {"en": "discord.gg/fortnitedev (PUBLIC)"},
                },
                {
                    "namespace": "Fortnite.FortAthenaMatchmakingWidget",
                    "key": "PrivateMatch",
                    "native_string": "Private",
                    "localized_strings": {"en": "discord.gg/fortnitedev (PRIVATE)"},
                },
                {
                    "namespace": "LoadingScreen",
                    "key": "Connecting",
                    "native_string": "CONNECTING",
                    "localized_strings": {"en": "Launching Fortnite (Boogie)"},
                },
                {
                    "namespace": "FortLoginStatus",
                    "key": "LoggingIn",
                    "native_string": "Logging In...",
                    "localized_strings": {"en": "Welcome to Boogie Hybrid!"},
                },
            ]

        return encode_patch(patch)

    default_runtime_options = encode_patch(
        {
            "scripts": {
                "/Script/FortniteGame.FortRuntimeOptions": {
                    "bEnableBlockedList": "false",
                    "bEnableNickname": "true ",
                    "bEnableEULA": "true",
                    "bShouldSkipAvailabilityCheck": "true",
                    "bEnableClientSettingsSaveToCloud": "false",
                }
            }
        }
    )

    @property
    def system_files(self):
        return json.dumps(
            [
                {
                    "uniqueFilename": "DefaultEngine.ini",
                    "filename": "DefaultEngine.ini",
                    "hash": sha1(self.default_engine),
                    "hash256": sha256(self.default_engine),
                    "length": len(self.default_engine.splitlines()),
                    "contentType": "application/octet-stream",
                    "uploaded": "someday",
                    "storageType": "S3",
                    "doNotCache": False,
                },
                {
                    "uniqueFilename": "DefaultGame.ini",
                    "filename": "DefaultGame.ini",
                    "hash": sha1(self.default_game),
                    "hash256": sha256(self.default_game),
                    "length": len(self.default_game.splitlines()),
                    "contentType": "application/octet-stream",
                    "uploaded": "someday",
                    "storageType": "S3",
                    "doNotCache": False,
                },
                {
                    "uniqueFilename": "DefaultRuntimeOptions.ini",
                    "filename": "DefaultRuntimeOptions.ini",
                    "hash": sha1(self.default_runtime_options),
                    "hash256": sha256(self.default_runtime_options),
                    "length": len(self.default_runtime_options.splitlines()),
                    "contentType": "application/octet-stream",
                    "uploaded": "someday",
                    "storageType": "S3",
                    "doNotCache": False,
                },
                {
                    "uniqueFilename": "config",
                    "filename": "config",
                    "hash": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
                    "hash256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "length": 0,
                    "contentType": "application/octet-stream",
                    "uploaded": "someday",
                    "storageType": "S3",
                    "doNotCache": False,
                },
            ]
        )
