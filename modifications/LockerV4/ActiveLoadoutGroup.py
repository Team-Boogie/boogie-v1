import json

from mitmproxy import http

import apis

from type_definitions import defaultUserSettings
from cosmetics import updateLoadout, getLoadout
from utils import config
from utils import checks
from utils import console_logs as logger


class ALG:
    def __init__(self, userSettings: defaultUserSettings):
        self.userSettings: defaultUserSettings = userSettings

    @checks.is_fortnite_request
    def response(self, flow: http.HTTPFlow):
        if not (
            "/locker/v4" in flow.request.url
            and flow.request.url.endswith("/active-loadout-group")
            and flow.request.method == "PUT"
        ):
            return

        accountId = flow.request.url.split("/")[8]
        lockerId = flow.request.url.split("/")[6]

        baseBody = flow.request.get_text()
        assert baseBody is not None
        body = json.loads(baseBody)

        loadouts = body["loadouts"]
        updateLoadout(loadouts=loadouts)
        
        isNiggaMode = config.read()["extraSettings"]["nigga_enabled"]
        
        try:
            if body["loadouts"]["CosmeticLoadout:LoadoutSchema_Character"][
                "loadoutSlots"
            ][0]["equippedItemId"].startswith("AthenaCharacter"):
                character = body["loadouts"]["CosmeticLoadout:LoadoutSchema_Character"][
                    "loadoutSlots"
                ][0]["equippedItemId"]
                apis.updateImage(
                    userImageUrl=f"https://fortnite-api.com/images/cosmetics/br/{character.split(":")[1]}/icon.png"
                )
        except:
            pass

        if isNiggaMode:
            try:  # reminder to add this as an option (nigga mode) or put this in  a seperate addon in exploits
                if body["loadouts"]["CosmeticLoadout:LoadoutSchema_Character"][
                    "loadoutSlots"
                ][0]["itemCustomizations"]:
                    for thing in body["loadouts"][
                        "CosmeticLoadout:LoadoutSchema_Character"
                    ]["loadoutSlots"][0]["itemCustomizations"]:
                        if thing.get("additionalData"):
                            thing["additionalData"] = "3CA3D70A3CA3D70A3CA3D70A3F800000"
            except:
                pass

        loadout = getLoadout(
            loadouts=body["loadouts"],
            accountId=accountId,
            lockerId=lockerId,
        )

        flow.response = http.Response.make(
            status_code=200,
            content=json.dumps(loadout),
            headers={"Content-Type": "application/json"},
        )
        logger.info("Cosmetic Check Detected")
