from datetime import datetime

import typing

import aiohttp

import type_definitions
import constants

from utils import translation
from utils import console_logs as logger
from utils import config
import apis

currentlyEquipped: dict[str, type_definitions.ActiveLoadoutLoadout] = {
    "CosmeticLoadout:LoadoutSchema_Emotes": {
        "loadoutSlots": [
            {
                "slotTemplate": "CosmeticLoadoutSlotTemplate:LoadoutSlot_Emote_0",
                "equippedItemId": "",
                "itemCustomizations": [],
            },
            {
                "slotTemplate": "CosmeticLoadoutSlotTemplate:LoadoutSlot_Emote_1",
                "itemCustomizations": [],
            },
            {
                "slotTemplate": "CosmeticLoadoutSlotTemplate:LoadoutSlot_Emote_2",
                "itemCustomizations": [],
            },
            {
                "slotTemplate": "CosmeticLoadoutSlotTemplate:LoadoutSlot_Emote_3",
                "itemCustomizations": [],
            },
            {
                "slotTemplate": "CosmeticLoadoutSlotTemplate:LoadoutSlot_Emote_4",
                "itemCustomizations": [],
            },
            {
                "slotTemplate": "CosmeticLoadoutSlotTemplate:LoadoutSlot_Emote_5",
                "itemCustomizations": [],
            },
        ],
        "shuffleType": "DISABLED",
    },
    "CosmeticLoadout:LoadoutSchema_Sparks": {"shuffleType": "DISABLED"},
    "CosmeticLoadout:LoadoutSchema_Jam": {"shuffleType": "DISABLED"},
    "CosmeticLoadout:LoadoutSchema_Vehicle": {"shuffleType": "DISABLED"},
    "CosmeticLoadout:LoadoutSchema_Vehicle_SUV": {"shuffleType": "DISABLED"},
    "CosmeticLoadout:LoadoutSchema_Character": {
        "loadoutSlots": [
            {
                "slotTemplate": "CosmeticLoadoutSlotTemplate:LoadoutSlot_Character",
                "itemCustomizations": [],
            },
            {
                "slotTemplate": "CosmeticLoadoutSlotTemplate:LoadoutSlot_Backpack",
                "itemCustomizations": [],
            },
            {
                "slotTemplate": "CosmeticLoadoutSlotTemplate:LoadoutSlot_Pickaxe",
                "equippedItemId": "",
                "itemCustomizations": [],
            },
            {
                "slotTemplate": "CosmeticLoadoutSlotTemplate:LoadoutSlot_Glider",
                "equippedItemId": "AthenaGlider:defaultglider",
                "itemCustomizations": [],
            },
            {
                "slotTemplate": "CosmeticLoadoutSlotTemplate:LoadoutSlot_Contrails",
                "itemCustomizations": [],
            },
            {
                "slotTemplate": "CosmeticLoadoutSlotTemplate:LoadoutSlot_Aura",
                "equippedItemId": "SparksAura:sparksaura_default",
                "itemCustomizations": [],
            },
        ],
        "shuffleType": "DISABLED",
    },
}


# async def buildAthena(
#     session: aiohttp.ClientSession,
#     storedCosmetics: list[dict[str, str]],
#     athena: dict[str, type_definitions.AthenaItem],
# ):

#     config_data: type_definitions.Config = config.read()
#     base: dict[str, type_definitions.AthenaItem] = {}

#     config_data = config.read()
#     async with session.get("https://fortniteapi.io//v2/items/list?fields=id,name,styles,type", headers={"Authorization": "4a676208-e51a441d-3edb8811-4b105253"}) as resp:
#         FortniteItems = await resp.json()

#     names: list[str] = []
#     ids: list[str] = []

#     for item in FortniteItems["items"]:
#         if item["id"] not in ids:

#             if not item["name"].strip():
#                 name: str = item["id"]
#             elif item["name"] in names:
#                 name: str = item["name"] + "-" + item["id"]
#             else:
#                 name: str = item["name"]

#             _id: str = item["id"]  # id is builtin func, don't name stuff after them
#             storedCosmetics.append(
#                 {"name": name, "id": _id, "type": item["type"]["id"]}
#             )
#             names.append(name)
#             ids.append(_id)

#     for item in FortniteItems["items"]:

#         variants: list[type_definitions.AthenaItemAttributesVariant] = []

#         if item.get("styles"):
#             styles = sorted(item["styles"], key=lambda x: x["channel"])

#             for channel, channel_styles_iter in groupby(styles, lambda x: x["channel"]):
#                 channel_styles = list(channel_styles_iter)
#                 variants.append(
#                     {
#                         "channel": channel.split(".")[-1],
#                         "active": channel_styles[0]["tag"].split(".")[-1],
#                         "owned": [
#                             style["tag"].split(".")[-1] for style in channel_styles
#                         ],
#                     }
#                 )
#         if item["type"]["id"] in str(constants.itemTypeMap):
#             templateId = constants.itemTypeMap[item["type"]["id"]] + ":" + item["id"]
#         else:
#             continue

#         itemTemplate: dict[str, type_definitions.AthenaItem] = {
#             templateId: {
#                 "templateId": templateId,
#                 "quantity": 1,
#                 "attributes": {
#                     "creation_time": None,
#                     "archived": (
#                         True if templateId in config_data["saved"]["archived"] else False
#                     ),
#                     "favorite": (
#                         True if templateId in config_data["saved"]["favorite"] else False
#                     ),
#                     "variants": variants,
#                     "item_seen": True,
#                     "giftFromAccountId": "4735ce9132924caf8a5b17789b40f79c",
#                 },
#             }
#         }
#         base.update(itemTemplate)

#     extraTemplates: list[dict[str, type_definitions.AthenaItem]] = [
#         {
#             "VictoryCrown_defaultvictorycrown": {
#                 "templateId": "VictoryCrown:defaultvictorycrown",
#                 "attributes": {
#                     "victory_crown_account_data": {
#                         "has_victory_crown": True,
#                         "data_is_valid_for_mcp": True,
#                         "total_victory_crowns_bestowed_count": 500,
#                         "total_royal_royales_achieved_count": 1942,
#                     },
#                     "max_level_bonus": 0,
#                     "level": 124,
#                     "item_seen": False,
#                     "xp": 0,
#                     "favorite": False,
#                 },
#                 "quantity": 1,
#             }
#         }
#     ]

#     for beanCharacter in [
#         "Character_BerryTartRiver",
#         "Character_BerryTartBrunt",
#         "CID_BeanCharacter_TEST",
#         "CID_BeanCharacter_Original",
#         "Bean_ZombieJonesy",
#         "Bean_ZombieElasticEB",
#         "Bean_RenegadeSkull",
#     ]:
#         extraTemplates.append(
#             {
#                 f"AthenaCharacter:{beanCharacter}": {
#                     "templateId": f"AthenaCharacter:{beanCharacter}",
#                     "quantity": 1,
#                     "attributes": {
#                         "creation_time": None,
#                         "archived": (
#                             True
#                             if f"AthenaCharacter:{beanCharacter}"
#                             in config_data["saved"]["archived"]
#                             else False
#                         ),
#                         "favorite": (
#                             True
#                             if f"AthenaCharacter:{beanCharacter}"
#                             in config_data["saved"]["favorite"]
#                             else False
#                         ),
#                         "item_seen": True,
#                         "giftFromAccountId": "4735ce9132924caf8a5b17789b40f79c",
#                     },
#                 }
#             }
#         )
#     for template in extraTemplates:
#         base.update(template)

#     config_data = config.read()

#     athena.update(base)
#     total: int = len(athena.keys())
#     logger.info(translation.get("console-stored-cosmetic").format(total))
#     try:
#         apis.updateCosmeticGraph(total)
#         apis.updateImage(
#             "https://fortnite-api.com//images/cosmetics/br/cid_028_athena_commando_f/icon.png"
#         )
#         # updateUserName(userName="Waiting for Launch...")
#     except:
#         pass
#     return len(FortniteItems["items"])


async def buildAthena(
    session: aiohttp.ClientSession,
    storedCosmetics: list[dict[str, str]],
    athena: dict[str, type_definitions.AthenaItem],
):

    config_data: type_definitions.Config = config.read()

    async with session.get(
        "https://fortnite-api.com/v2/cosmetics",
    ) as resp:
        FortniteItems = await resp.json()

    names: list[str] = []
    ids: list[str] = []

    for mode in FortniteItems["data"]:
        if mode in ("lego", "beans"):
            continue

        for item in FortniteItems["data"][mode]:
            if "random" in item["id"].lower():
                continue

            if mode == "tracks":
                item["type"] = {"backendValue": "SparksSong", "value": "SparksSong"}

            item["type"]["backendValue"] = constants.dash_api_map.get(
                item["type"]["backendValue"], item["type"]["backendValue"]
            )

            if item["id"] not in ids:
                name: str = item.get("name", "")

                if not name.strip():
                    name = item["id"]
                elif name in names:
                    name = f"{name} ({item["id"]})"
                else:
                    names.append(name)

                storedCosmetics.append(
                    {"name": name, "id": item["id"], "type": item["type"]["value"]}
                )

                ids.append(item["id"])

            templateId = f"{item["type"]["backendValue"]}:{item["id"]}"

            variants: list[type_definitions.AthenaItemAttributesVariant] = []

            if item.get("variants"):
                for obj in item["variants"]:
                    variants.append(
                        {
                            "channel": obj.get("channel", ""),
                            "active": (
                                obj.get("options", [])[0:1]
                                or [typing.cast(dict[str, str], {})]
                            )[0].get("tag", ""),
                            "owned": [
                                variant.get("tag", "")
                                for variant in obj.get("options", [])
                            ],
                        }
                    )

            athena[templateId] = {
                "templateId": templateId,
                "attributes": {
                    "max_level_bonus": 0,
                    "level": 1,
                    "item_seen": True,
                    "xp": 0,
                    "variants": variants,
                    "archived": (
                        True
                        if templateId in config_data["saved"]["archived"]
                        else False
                    ),
                    "favorite": (
                        True
                        if templateId in config_data["saved"]["favorite"]
                        else False
                    ),
                    "giftFromAccountId": "4735ce9132924caf8a5b17789b40f79c",
                },
                "quantity": 1,
            }

    total: int = len(athena)

    logger.info(translation.get("console-stored-cosmetic").format(total))

    try:
        apis.updateCosmeticGraph(total)
        apis.updateImage(
            "https://fortnite-api.com//images/cosmetics/br/cid_028_athena_commando_f/icon.png"
        )
    except:
        pass
    return total


def activeLoadouts(accountId: str, lockerId: str):
    config_data: type_definitions.Config = config.read()

    baseLoadoutDict: type_definitions.LockerV3Items = {
        "activeLoadoutGroup": {
            "deploymentId": lockerId,
            "accountId": accountId,
            "athenaItemId": "867bb1fc-ffd5-4be6-9b0c-57427e5cb2a8",
            "creationTime": str(
                object=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            ),
            "updatedTime": str(
                object=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            ),
            "loadouts": {},
        },
        "loadoutGroupPresets": [],
        "loadoutPresets": [],
    }

    # resp = []

    for preset in config_data["saved"]["presets"].values():
        preset.update(
            {
                "deploymentId": lockerId,
                "accountId": accountId,
                "loadoutType": "CosmeticLoadout:LoadoutSchema_Character",
                "presetId": "0001",
                "presetIndex": 1,
                "athenaItemId": "e0b2bd58-b74a-40d5-88e7-8b87dc69de2e",
                "creationTime": "2024-08-26T22:53:24.485687980Z",
                "updatedTime": "2024-08-26T22:53:24.485687980Z",
            }
        )
        logger.info(f"Loaded {preset['presetIndex']} preset")
        baseLoadoutDict["loadoutGroupPresets"].append(preset)

    for equipped in currentlyEquipped:
        loadoutType = equipped
        try:
            baseLoadoutDict["activeLoadoutGroup"]["loadouts"].update(
                {loadoutType: currentlyEquipped[loadoutType]}
            )
        except KeyError:
            pass

    return baseLoadoutDict


def getLoadout(
    loadouts: dict[str, type_definitions.ActiveLoadoutLoadout],
    accountId: str,
    lockerId: str,
):

    loadoutInfo: type_definitions.ActiveLoadout = {
        "deploymentId": lockerId,
        "accountId": accountId,
        "athenaItemId": "867bb1fc-ffd5-4be6-9b0c-57427e5cb2a8",
        "creationTime": "2024-11-03T04:12:55.785Z",
        "loadouts": loadouts,
    }

    return loadoutInfo


def updateLoadout(
    loadouts: dict[str, type_definitions.ActiveLoadoutLoadout],
):  # , #loadoutSlots: list[ActiveLoadoutSlot]):
    global currentlyEquipped
    currentlyEquipped = loadouts
    return currentlyEquipped
