import traceback
import xml.etree.ElementTree as ET

import typing
import aiohttp
import json

from datetime import datetime
from mitmproxy import http

import apis
import type_definitions
import constants

from utils import config
from utils import console_logs as logger, epicgames
from utils.blurl import compress_json_content

nameExploit: bool = False
nameOld: str = "just pirxcy"
nameNew: str = "🇵🇸"

global displayName
displayName = ""


class Addon:
    def __init__(
        self,
        athena: dict[str, type_definitions.AthenaItem],
        userSettings: type_definitions.defaultUserSettings,
        common_core: dict[str, type_definitions.AthenaItem],
        session: aiohttp.ClientSession
    ):
        self.athena = athena
        self.userSettings = userSettings
        self.common_core = common_core
        self.revisionAdd = 1
        self.hasGift = False
        self.session = session

    async def get_access_token(self) -> str:
        remember_me_data: type_definitions.RememberMe = epicgames.get_remember_me_data()
        refresh_token = remember_me_data["Token"]

        async with self.session.post(
            "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
            auth=aiohttp.BasicAuth(
                "34a02cf8f4414e29b15921876da36f9a",
                "daafbccc737745039dffe53d94fc76cf",
            ),
            data={"grant_type": "refresh_token", "refresh_token": refresh_token},
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()

        remember_me_data["Token"] = data["refresh_token"]
        epicgames.set_remember_me_data(remember_me_data)

        return data["access_token"]

    async def request(self, flow: http.HTTPFlow) -> None:
        url: str = flow.request.pretty_url
        userAgent: str = str(
            object=flow.request.headers.get("User-Agent", default=None)
        )
        gameVersion: str = epicgames.getFortniteVersion()
        userAgents: list[str] = epicgames.getUserAgents(gameVersion)
        splitUserAgent = userAgent.split(sep="/")
        if len(splitUserAgent) >= 2:
            correctedUserAgent = splitUserAgent[1].replace(" ", "-")
        else:
            correctedUserAgent = userAgent

        auth = flow.request.headers.get("Authorization", default="")
        if auth.startswith("bearer ") and self.userSettings["accountId"] == "":
            try:
                async with self.session.get(
                    "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/verify",
                    headers={"Authorization": auth},
                ) as resp:
                    jsonData = await resp.json()

                self.userSettings["accountId"] = jsonData["account_id"]

                async with self.session.get(
                    f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{jsonData['account_id']}",
                    headers={"Authorization": auth},
                ) as resp:
                    data = await resp.json()

                try:
                    print(self.userSettings["displayName"]*100)
                    await apis.updateUserName(self.userSettings, data["displayName"])
                    self.userSettings["displayName"] = data["displayName"]
                    if type_definitions.Badge.epicgames not in self.userSettings["badges"]:
                        self.userSettings["badges"].append(type_definitions.Badge.epicgames)
                        apis.updateUserBadges(self.userSettings["badges"])# carry on from here :)i
                except KeyError:
                    pass
                except RuntimeError:
                    pass

                async with self.session.get(f"{constants.URLs.COMMANDO}/users") as resp:
                    usersdata: str = await resp.text()
                try:
                    apis.updateUsers(int(usersdata))
                except ValueError:
                    apis.updateUsers(-1)

            except KeyError:
                pass

        if userAgent in userAgents or correctedUserAgent in userAgents:
            if url.lower().startswith(
                "https://eulatracking-public-service-prod06.ol.epicgames.com/eulatracking/api/public/agreements/fn/account/"
            ):
                logger.info(msg="Fortnite Start Detected")

            if nameExploit:
                try:
                    assert flow.response is not None
                    request_text = flow.request.get_text()
                    assert request_text is not None
                    flow.request.url = flow.request.url.replace(nameOld, nameNew)
                    body = json.loads(request_text)
                    # replace all instances of nameOld in the body with nameNew
                    body = json.loads(json.dumps(body).replace(nameOld, nameNew))
                    flow.response.text = str(object=json.dumps(obj=body))
                except:
                    pass

            if "queryprofile" in url.lower() and "rvn=-1" not in url.lower():
                flow.request.url = url.split("rvn=")[0] + "rvn=-1"
                flow.request.headers.pop("X-EpicGames-ProfileRevisions")  # not my fault
                print(flow.request.url + "modified")

            if (
                "https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/matchmakingservice/ticket/player"
                in flow.request.pretty_url
                and self.userSettings["premium"]
            ):
                flow.request.url = flow.request.url.replace(
                    # "%3A" + "playlist_nobuildbr_squad",
                    "playlist_nobuildbr_squad",
                    config.read()["extraSettings"]["playlist"],
                    # "%3A" + "playlist_figmentsolo"
                ).replace(
                    f'&player.option.linkCode={config.read()["extraSettings"]["playlist"]}',
                    "",
                )
                logger.info(f"Matchmaking: {flow.request.url}")

            if url.startswith(
                "https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/storeaccess/v1/request_access/"
            ):
                accountId = str(object=url.split(sep="/")[1:])
                flow.request.url = flow.request.url.replace(
                    accountId,
                    "cfd16ec54126497ca57485c1ee1987dc",  # SypherPK's AccountID
                )

            if "RemoveGiftBox" in url.lower():
                text: str = str(object=flow.request.get_text())
                requestBody = json.loads(text)
                print(requestBody["giftBoxItemIds"])
                for item in requestBody["giftBoxItemIds"]:
                    try:
                        del self.common_core[item]
                        del self.athena[item]
                        print("Removed gift " + item)
                    except Exception as e:
                        print(f"no giftbox remove {e}")
                self.hasGift = bool(len(self.common_core.keys()))

            elif (
                "https://payment-website-pci.ol.epicgames.com/payment/v1/purchase"
                in url
            ):
                flow.request.url = f"{constants.URLs.CDN}/sa.mp4"

            if ".blurl" in url:

                if (
                    self.userSettings["premium"]
                    and self.userSettings["savedUrl"] is not None
                ):
                    url = self.userSettings["savedUrl"]
                else:
                    url = f"{constants.URLs.CDN}/maeko.mp4"

                playlist: dict[str, list[dict[str, str | float]]] = {
                    "playlists": [
                        {
                            "type": "main",
                            "language": "en",
                            "url": url,
                            "data": '<?xml version="1.0" encoding="utf-8"?><MPD xmlns="urn:mpeg:dash:schema:mpd:2011" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="urn:mpeg:DASH:schema:MPD:2011 http://standards.iso.org/ittf/PubliclyAvailableStandards/MPEG-DASH_schema_files/DASH-MPD.xsd" xmlns:clearkey="http://dashif.org/guidelines/clearKey" xmlns:cenc="urn:mpeg:cenc:2013" profiles="urn:mpeg:dash:profile:isoff-live:2011" type="static" mediaPresentationDuration="PT1H8M10.700S" minBufferTime="PT4.000S"><ProgramInformation></ProgramInformation><Period id="0" start="PT0S"><AdaptationSet id="0" contentType="audio" segmentAlignment="true" bitstreamSwitching="true"><Representation id="0" audioSamplingRate="48000" bandwidth="128000" mimeType="audio/mp4" codecs="mp4a.40.2"><SegmentTemplate duration="2000000" timescale="1000000" initialization="init_ar_AR_$RepresentationID$.mp4" media="segment_ar_AR_$RepresentationID$_$Number$.m4s" startNumber="1"></SegmentTemplate><AudioChannelConfiguration schemeIdUri="urn:mpeg:dash:23003:3:audio_channel_configuration:2011" value="2"></AudioChannelConfiguration></Representation><ContentProtection schemeIdUri="urn:mpeg:dash:mp4protection:2011" value="cenc" cenc:default_KID="aceaae98-5754-0f4a-483e-25861a192e55"></ContentProtection><ContentProtection schemeIdUri="urn:uuid:e2719d58-a985-b3c9-781a-b030af78d30e" value="ClearKey1.0"><clearkey:Laurl Lic_type="EME-1.0">key.key</clearkey:Laurl></ContentProtection></AdaptationSet></Period></MPD>',
                            "duration": 4113.700121999999,
                        }
                    ]
                }
                flow.response = http.Response.make(
                    200,
                    content=compress_json_content(playlist),
                )

            if "/client/" in flow.request.url:
                logger.fortnite(msg=f"{flow.request.url}")

        elif (
            (".png" in url or ".jpg" in url or ".jpeg" in url)
            and (".epic" in url or ".unreal" in url or ".static" in url)
            and (
                (not self.userSettings["premium"])
                or (
                    self.userSettings["premium"]
                    and config.read()["extraSettings"]["images_enabled"]
                )
            )
        ):
            if self.userSettings["premium"]:
                if config.read()["extraSettings"]["images_enabled"]:
                    flow.request.url = config.read()["extraSettings"]["image"]
            else:
                flow.request.url = f"{constants.URLs.CDN}/SplashScreen.png"

    def websocket_message(self, flow: http.HTTPFlow):
        assert flow.websocket is not None
        clientMsg = bool(flow.websocket.messages[-1].from_client)
        msg = str(object=flow.websocket.messages[-1])
        msg: str = str(object=msg).replace('"WIN"', '"PS5"')
        msg = msg[1:-1]
        msg = msg

        if "match" in flow.request.pretty_url.lower():
            logger.info(msg="Matchmaking Started!")

        elif "xmpp" in flow.request.pretty_url.lower():
            self.userSettings["xmppFlow"] = flow
            if clientMsg:
                root = ET.fromstring(msg)
                if root.attrib.get("id") == "_xmpp_bind1":
                    namespace = "urn:ietf:params:xml:ns:xmpp-bind"
                    namespaceresource = root.find(f".//{{{namespace}}}resource")
                    assert namespaceresource is not None
                    assert namespaceresource.text is not None
                    jid: str = namespaceresource.text
                    self.userSettings["jid"] = jid  # :) it works tho i tested that part
                else:
                    status_element = root.find("status")
                    if status_element is None:
                        return
                    assert status_element.text is not None
                    json_data = json.loads(status_element.text)

                    if self.userSettings["premium"]:
                        json_data["Status"] = config.read()["extraSettings"]["status"]
                    else:
                        json_data["Status"] = "👉 discord.gg/fortnitedev 🚀🗿"

                    new_json_text = json.dumps(json_data)

                    status_element.text = new_json_text
                    new_xml_data: bytes = ET.tostring(root)

                    flow.websocket.messages[-1].content = new_xml_data

    async def response(
        self, flow: http.HTTPFlow
    ):  # called after server responds but before the response is sent to the client
        url: str = flow.request.pretty_url
        userAgent: str = str(
            object=flow.request.headers.get("User-Agent", default=None)  # not my fault
        )
        gameVersion: str = epicgames.getFortniteVersion()
        userAgents: list[str] = epicgames.getUserAgents(gameVersion)
        splitUserAgent = userAgent.split(sep="/")
        if len(splitUserAgent) >= 2:
            correctedUserAgent = splitUserAgent[1].replace(" ", "-")
        else:
            correctedUserAgent = userAgent

        if userAgent in userAgents or gameVersion in correctedUserAgent:

            if (
                "epicgames.com/account/api/oauth/"
                in url.lower()
            ):
                assert flow.response is not None
                baseBody = flow.response.get_text()
                assert baseBody is not None

                body = json.loads(baseBody)
                if body.get("displayName"):
                    if body.get("account_id"):
                        self.userSettings["accountId"] = body["account_id"]
                    await apis.updateUserName(self.userSettings, body["displayName"])
                    self.userSettings["displayName"] = body["displayName"]
                    logger.info(f"{self.userSettings["displayName"]} logged in.")
                    print(self.userSettings)
                    self.userSettings["badges"].append(type_definitions.Badge.epicgames)
                    apis.updateUserBadges(self.userSettings["badges"])

            if (
                ("setloadoutshuffleenabled" in url.lower())
                or url
                == "https://fortnitewaitingroom-public-service-prod.ol.epicgames.com/waitingroom/api/waitingroom"
                or "socialban/api/public/v1" in url.lower()
            ):
                flow.response = http.Response.make(
                    status_code=204,
                    content=b"",
                    headers={"Content-Type": "text/html"},
                )  # Return no body

            if "/loadout-group-preset/index/" in url.lower():
                indexSlot: str = url.split("/")[11]
                lockerId: str = url.split("/")[6]
                accountId: str = url.split("/")[8]

                baseBody = flow.request.get_text()
                assert baseBody is not None
                body = json.loads(baseBody)

                presetName: str = body["displayName"]
                presetIndex: int = body["presetIndex"]
                athenaItemId: str = body["athenaItemId"]

                presetLoadouts: type_definitions.PresetResponseLoadouts = body[
                    "loadouts"
                ]

                presetLoadouts.update(
                    {
                        "displayName": presetName,
                        "presetIndex": presetIndex,
                        "presetFavoriteStatus": "EMPTY",
                        "presetId": str(presetIndex).zfill(4),
                        "presetIndex": presetIndex,
                    }
                )

                configLoadout: type_definitions.PresetResponseLoadouts = {
                    "deploymentId": lockerId,
                    "accountId": accountId,
                    "presetId": str(presetIndex).zfill(4),
                    "presetIndex": presetIndex,
                    "athenaItemId": athenaItemId,
                    "creationTime": str(
                        object=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
                        + "Z"
                    ),
                    "updatedTime": str(
                        object=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
                        + "Z"
                    ),
                    "loadouts": presetLoadouts,
                }

                config_data: type_definitions.Config = config.read()

                config_data["saved"]["presets"].update({str(indexSlot): configLoadout})

                with open(constants.configFilePath, "w") as f:
                    json.dump(config_data, f, indent=2)

                newresponse: type_definitions.PresetResponse = {
                    "accountId": accountId,
                    "athenaItemId": athenaItemId,
                    "creationTime": str(
                        object=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
                        + "Z"
                    ),
                    "deploymentId": lockerId,
                    "displayName": presetName,
                    "loadouts": presetLoadouts,
                    "presetFavoriteStatus": "EMPTY",
                    "presetId": str(presetIndex).zfill(4),
                    "presetIndex": presetIndex,
                    "updatedTime": str(
                        object=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
                        + "Z"
                    ),
                }

                flow.response = http.Response.make(
                    status_code=200,
                    content=json.dumps(newresponse),
                    headers={"Content-Type": "application/json"},
                )

            if "putmodularcosmetic" in url.lower():
                logger.info("Cosmetic Change Detected.")

                presetMap: dict[str, str] = {
                    "CosmeticLoadout:LoadoutSchema_Character": "character",
                    "CosmeticLoadout:LoadoutSchema_Emotes": "emotes",
                    "CosmeticLoadout:LoadoutSchema_Platform": "lobby",
                    "CosmeticLoadout:LoadoutSchema_Wraps": "wraps",
                    "CosmeticLoadout:LoadoutSchema_Jam": "jam",
                    "CosmeticLoadout:LoadoutSchema_Sparks": "instruments",
                    "CosmeticLoadout:LoadoutSchema_Vehicle": "sports",
                    "CosmeticLoadout:LoadoutSchema_Vehicle_SUV": "suv",
                }

                baseBody = flow.request.get_text()
                assert baseBody is not None
                body = json.loads(baseBody)
                loadoutData = json.loads(body["loadoutData"])
                loadoutType: str = body["loadoutType"]

                if "CosmeticLoadout:LoadoutSchema_Character" == loadoutType:
                    apis.updateImage(
                        userImageUrl=f"https://fortnite-api.com/images/cosmetics/br/{loadoutData['slots'][0]['equipped_item'].split(":")[1]}/icon.png"
                    )

                loadoutPresets: type_definitions.LoadoutPresets = {
                    "CosmeticLoadout:LoadoutSchema_Character": {},
                    "CosmeticLoadout:LoadoutSchema_Emotes": {},
                    "CosmeticLoadout:LoadoutSchema_Platform": {},
                    "CosmeticLoadout:LoadoutSchema_Wraps": {},
                    "CosmeticLoadout:LoadoutSchema_Jam": {},
                    "CosmeticLoadout:LoadoutSchema_Sparks": {},
                    "CosmeticLoadout:LoadoutSchema_Vehicle": {},
                    "CosmeticLoadout:LoadoutSchema_Vehicle_SUV": {},
                }

                if body.get("presetId") != 0:
                    presetId: int = body["presetId"]

                    slots: list[type_definitions.ConfigSavedPresetSlot] = loadoutData[
                        "slots"
                    ]
                    presetType: str = body["loadoutType"]

                    configTemplate: type_definitions.ConfigSavedPreset = {
                        "presetType": presetType,
                        "presetId": presetId,
                        "slots": slots,
                    }

                    with open(constants.configFilePath) as f:
                        data: type_definitions.Config = json.load(f)

                    key = presetMap.get(presetType)

                    assert key is not None
                    typing.cast(
                        dict[str, type_definitions.ConfigSavedPreset],
                        data["saved"]["presets"][key],
                    ).update({str(object=presetId): configTemplate})

                    self.athena.update(
                        {
                            f"{presetType} {presetId}": {
                                "attributes": {
                                    "display_name": f"PRESET {presetId}",
                                    "slots": slots,
                                },
                                "quantity": 1,
                                "templateId": presetType,
                            },
                        }
                    )

                    with open(constants.configFilePath, mode="w") as f:
                        json.dump(obj=data, fp=f, indent=2)

                    typing.cast(dict[int, str], loadoutPresets[presetType]).update(
                        {presetId: f"{presetType} {presetId}"}
                    )

                splitURL = url.split("/")
                if len(splitURL) >= 9:
                    accountId = splitURL[8]
                else:
                    accountId = "cfd16ec54126497ca57485c1ee1987dc"  # SypherPK's ID

                response: type_definitions.AthenaResponse = {
                    "profileRevision": 99999,
                    "profileId": "self.athena",
                    "profileChangesBaseRevision": 99999,
                    "profileCommandRevision": 99999,
                    "profileChanges": [
                        {
                            "changeType": "fullProfileUpdate",
                            "profile": {
                                "created": "",
                                "updated": str(
                                    object=datetime.now().strftime(
                                        "%Y-%m-%dT%H:%M:%S.%f"
                                    )[:-3]
                                    + "Z"
                                ),
                                "rvn": 0,
                                "wipeNumber": 1,
                                "accountId": accountId,
                                "profileId": "self.athena",
                                "version": "no_version",
                                "items": self.athena,
                                "stats": {"loadout_presets": loadoutPresets},
                                "commandRevision": 99999,
                                "profileCommandRevision": 99999,
                                "profileChangesBaseRevision": 99999,
                            },
                        }
                    ],
                }

                flow.response = http.Response.make(
                    status_code=200,
                    content=json.dumps(obj=response),
                    headers={"Content-Type": "application/json"},
                )

            if "SetItemFavoriteStatusBatch" in url:
                logger.info(msg=f"Cosmetic favorite detected.")

                text: str = str(flow.request.get_text())
                favData = json.loads(str(object=text))

                changeValue = favData["itemFavStatus"][0]
                itemIds: list[str] = favData["itemIds"]

                if changeValue:

                    with open(constants.configFilePath) as f:
                        data: type_definitions.Config = json.load(f)

                    for itemId in itemIds:
                        if itemId not in data["saved"]["favorite"]:
                            data["saved"]["favorite"].append(itemId)
                        self.athena[itemId]["attributes"]["favorite"] = True

                    with open(constants.configFilePath, mode="w") as fs:
                        json.dump(data, fs, indent=2)
                else:

                    with open(constants.configFilePath) as f:
                        data: type_definitions.Config = json.load(f)

                    for itemId in itemIds:
                        if itemId in data["saved"]["favorite"]:
                            data["saved"]["favorite"].remove(itemId)
                        self.athena[itemId]["attributes"]["favorite"] = False

                    with open(constants.configFilePath, mode="w") as f:
                        json.dump(data, f, indent=2)
                splitURL = url.split("/")
                if len(splitURL) >= 9:
                    accountId = splitURL[8]
                else:
                    accountId = "cfd16ec54126497ca57485c1ee1987dc"  # SypherPK's ID

                response = {
                    "profileRevision": 99999,
                    "profileId": "athena",
                    "profileChangesBaseRevision": 99999,
                    "profileCommandRevision": 99999,
                    "profileChanges": [
                        {
                            "changeType": "fullProfileUpdate",
                            "profile": {
                                "created": "",
                                "updated": str(
                                    object=datetime.now().strftime(
                                        "%Y-%m-%dT%H:%M:%S.%f"
                                    )[:-3]
                                    + "Z"
                                ),
                                "rvn": 0,
                                "wipeNumber": 1,
                                "accountId": accountId,
                                "profileId": "athena",
                                "version": "no_version",
                                "items": self.athena,
                                "commandRevision": 99999,
                                "profileCommandRevision": 99999,
                                "profileChangesBaseRevision": 99999,
                            },
                        }
                    ],
                }

                flow.response = http.Response.make(
                    status_code=200,
                    content=json.dumps(response),
                    headers={"Content-Type": "application/json"},
                )

            if "/SetItemArchivedStatusBatch" in url:
                logger.info(msg=f"Cosmetic archive detected.")

                text = str(object=flow.request.get_text())
                archiveData = json.loads(str(object=text))

                changeValue = archiveData["archived"]
                itemIds = archiveData["itemIds"]

                if changeValue:

                    data = config.read()

                    for itemId in itemIds:
                        self.athena[itemId]["attributes"]["archived"] = True
                        if itemId not in data["saved"]["archived"]:
                            data["saved"]["archived"].append(itemId)
                    with open(constants.configFilePath, mode="w") as f:
                        json.dump(data, f, indent=2)
                else:

                    with open(constants.configFilePath) as f:
                        data: type_definitions.Config = json.load(f)

                    for itemId in itemIds:
                        self.athena[itemId]["attributes"]["archived"] = False
                        if itemId not in data["saved"]["archived"]:
                            data["saved"]["archived"].remove(itemId)

                    with open(constants.configFilePath, mode="w") as f:
                        json.dump(obj=data, fp=f, indent=2)

                splitURL = url.split("/")
                if len(splitURL) >= 9:
                    accountId = splitURL[8]
                else:
                    accountId = "cfd16ec54126497ca57485c1ee1987dc"  # SypherPK's ID

                response = {
                    "profileRevision": 99999,
                    "profileId": "athena",
                    "profileChangesBaseRevision": 99999,
                    "profileCommandRevision": 99999,
                    "profileChanges": [
                        {
                            "changeType": "fullProfileUpdate",
                            "profile": {
                                "created": "",
                                "updated": str(
                                    object=datetime.now().strftime(
                                        "%Y-%m-%dT%H:%M:%S.%f"
                                    )[:-3]
                                    + "Z"
                                ),
                                "rvn": 0,
                                "wipeNumber": 1,
                                "accountId": accountId,
                                "profileId": "athena",
                                "version": "no_version",
                                "items": self.athena,
                                "commandRevision": 99999,
                                "profileCommandRevision": 99999,
                                "profileChangesBaseRevision": 99999,
                            },
                        }
                    ],
                }

                flow.response = http.Response.make(
                    status_code=200,
                    content=json.dumps(response),
                    headers={"Content-Type": "application/json"},
                )
            if "#setcosmeticlockerslot" in url.lower():
                splitURL = url.split("/")
                if len(splitURL) >= 9:
                    accountId = splitURL[8]
                else:
                    accountId = "cfd16ec54126497ca57485c1ee1987dc"  # SypherPK's ID

                response = {
                    "profileRevision": 99999,
                    "profileId": "athena",
                    "profileChangesBaseRevision": 99999,
                    "profileCommandRevision": 99999,
                    "profileChanges": [
                        {
                            "changeType": "fullProfileUpdate",
                            "profile": {
                                "created": "",
                                "updated": str(
                                    object=datetime.now().strftime(
                                        "%Y-%m-%dT%H:%M:%S.%f"
                                    )[:-3]
                                    + "Z"
                                ),
                                "rvn": 0,
                                "wipeNumber": 1,
                                "accountId": accountId,
                                "profileId": "athena",
                                "version": "no_version",
                                "items": self.athena,
                                "commandRevision": 99999,
                                "profileCommandRevision": 99999,
                                "profileChangesBaseRevision": 99999,
                            },
                        }
                    ],
                }
                flow.response = http.Response.make(
                    status_code=200,
                    content=json.dumps(response),
                    headers={"Content-Type": "application/json"},
                )

            if (
                url.lower().startswith(
                    "https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/matchmaking/session/"
                )
                and flow.request.method == "GET"
            ):
                assert flow.response is not None
                assert flow.response.text is not None
                text = flow.response.text
                matchData = json.loads(str(object=text))

                matchData["allowInvites"] = True  # Alllow Invites Mid-Game
                matchData["allowJoinInProgress"] = True  # Join via Profile
                matchData["allowJoinViaPresence"] = True  # Join via Lobby

                matchData["allowJoinViaPresenceFriendsOnly"] = (
                    False  # Friends only join
                )
                matchData["attributes"]["ALLOWBROADCASTING_b"] = False
                matchData["attributes"]["ALLOWMIGRATION_s"] = "true"
                matchData["attributes"]["ALLOWREADBYID_s"] = "true"
                matchData["attributes"][
                    "CHECKSANCTIONS_s"
                ] = "false"  # Check for any bans
                matchData["attributes"][
                    "REJOINAFTERKICK_s"
                ] = "OPEN"  # Ability to rejoin after kick
                matchData["attributes"]["allowMigration_s"] = True
                matchData["attributes"]["allowReadById_s"] = True
                matchData["attributes"]["checkSanctions_s"] = False
                matchData["attributes"]["rejoinAfterKick_s"] = True

                matchData["shouldAdvertise"] = True
                matchData["usesPresence"] = True
                matchData["usesStats"] = False
                matchData["maxPrivatePlayers"] = 999
                matchData["maxPublicPlayers"] = 999
                matchData["openPrivatePlayers"] = 999
                matchData["openPublicPlayers"] = 999

                flow.response.text = json.dumps(obj=matchData)

            if (
                "client/QueryProfile?profileId=athena" in url
                or "client/ClientQuestLogin?profileId=athena" in url
            ):
                assert flow.response is not None
                text = str(object=flow.response.get_text())
                athenaFinal = json.loads(text)
                settings = config.read()["extraSettings"]
                try:
                    athenaFinal["profileChanges"][0]["profile"]["items"] = self.athena
                    athenaFinal["profileChanges"][0]["profile"]["stats"]["attributes"][
                        "level"
                    ] = settings["levels"]
                    athenaFinal["profileChanges"][0]["profile"]["stats"]["attributes"][
                        "battlestars"
                    ] = settings["battlestars"]
                    athenaFinal["profileChanges"][0]["profile"]["items"][
                        "VictoryCrown_defaultvictorycrown"
                    ] = {
                        "templateId": "VictoryCrown:defaultvictorycrown",
                        "attributes": {
                            "victory_crown_account_data": {
                                "has_victory_crown": True,
                                "data_is_valid_for_mcp": True,
                                "total_victory_crowns_bestowed_count": 500,
                                "total_royal_royales_achieved_count": settings[
                                    "crowns"
                                ],
                            },
                            "max_level_bonus": 0,
                            "level": 124,
                            "item_seen": False,
                            "xp": 0,
                            "favorite": False,
                        },
                        "quantity": 1,
                    }
                    flow.response.text = str(object=json.dumps(obj=athenaFinal))
                except:
                    pass

            if (
                "client/QueryProfile?profileId=common_core" in url
                or "client/RemoveGiftBox?profileId=common_core" in url
            ):
                assert flow.response is not None
                text = str(object=flow.response.get_text())
                respText = str(object=flow.request.get_text())
                settings = config.read()["extraSettings"]
                commonFinal = json.loads(text)
                try:
                    commonFinal["profileRevision"] += self.revisionAdd
                    commonFinal["profileChangesBaseRevision"] += self.revisionAdd
                    commonFinal["profileCommandRevision"] += self.revisionAdd
                    if len(commonFinal["profileChanges"]) != 0:
                        commonFinal["profileChanges"][0]["profile"][
                            "rvn"
                        ] += self.revisionAdd
                        commonFinal["profileChanges"][0]["profile"]["updated"] = (
                            datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
                        )

                        for item in commonFinal["profileChanges"][0]["profile"][
                            "items"
                        ].values():
                            if item["templateId"] == "Currency:MtxPurchased":
                                item["quantity"] = settings["vbucks"]

                        commonFinal["profileChanges"][0]["profile"]["items"].update(
                            self.athena
                        )

                        commonFinal["profileChanges"][0]["profile"]["items"].update(
                            self.common_core
                        )
                    if "client/RemoveGiftBox?profileId=common_core" in url:
                        giftBoxItemIds = json.loads(respText)["giftBoxItemIds"]
                        commonFinal["profileChanges"] = [
                            {"changeType": "itemRemoved", "itemId": giftboxID}
                            for giftboxID in giftBoxItemIds
                        ]

                    self.revisionAdd += 1
                    flow.response.text = str(object=json.dumps(commonFinal))
                except:
                    print(traceback.format_exc())

            if (
                "/fortnite/api/matchmaking/session/" in url.lower()
                and "/join" in url.lower()
            ):
                flow.response = http.Response.make(
                    status_code=200,
                    content=b"[]",
                    headers={"Content-Type": "application/json"},
                )  # no body

            if "/lightswitch/api/service/bulk/status" in url.lower():
                # Launch Fortnite During Downtimes.
                status: list[type_definitions.LightswitchService] = [
                    {
                        "serviceInstanceId": "fortnite",
                        "status": "UP",
                        "message": "fortnite is up.",
                        "maintenanceUri": None,
                        "overrideCatalogIds": ["a7f138b2e51945ffbfdacc1af0541053"],
                        "allowedActions": ["PLAY", "DOWNLOAD"],
                        "banned": False,
                        "launcherInfoDTO": {
                            "appName": "Fortnite",
                            "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
                            "namespace": "fn",
                        },
                    }
                ]
                dump: str = json.dumps(status)
                assert flow.response is not None
                flow.response.text = dump

            if (
                "/lfg/fortnite/tags" in url.lower()
                and self.userSettings["premium"] == True
            ):
                data = config.read()
                users: list[str] = data["InviteExploit"]["users"]
                assert flow.response is not None
                flow.response.text = json.dumps(obj={"users": users})
                logger.info(url)
