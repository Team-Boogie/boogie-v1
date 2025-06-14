import json

from mitmproxy import http

from type_definitions import defaultUserSettings, ActiveLoadout
from cosmetics import activeLoadouts
from utils import checks
from utils import console_logs as logger


class QI:
    def __init__(self, userSettings: defaultUserSettings):
        self.userSettings: defaultUserSettings = userSettings

    @checks.is_fortnite_request
    def response(self, flow: http.HTTPFlow):
        try:
            if not (
                "/locker/v4" in flow.request.url
                and flow.request.url.endswith("/items")
                and flow.request.method == "GET"
            ):
                return

            baseBody = flow.request.get_text()
            assert baseBody is not None
            try:
                body = json.loads(baseBody)
            except:
                print(baseBody)
                return

            activeLoadoutGroup: ActiveLoadout = body["activeLoadoutGroup"]

            accountId = flow.request.url.split("/")[8]
            lockerId = flow.request.url.split("/")[6]

            self.userSettings["lockerId"] = lockerId
            assert "deploymentId" in activeLoadoutGroup
            assert "updatedTime" in activeLoadoutGroup
            self.userSettings["deploymentId"] = activeLoadoutGroup["deploymentId"]
            self.userSettings["athenaItemId"] = activeLoadoutGroup["athenaItemId"]
            self.userSettings["creationTime"] = activeLoadoutGroup["creationTime"]
            self.userSettings["updatedTime"] = activeLoadoutGroup["updatedTime"]

            loadout = activeLoadouts(
                accountId=accountId,
                lockerId=lockerId,
            )

            flow.response = http.Response.make(
                status_code=200,
                content=json.dumps(loadout),
                headers={"Content-Type": "application/json"},
            )

            logger.info("Lobby Loadout Check Detected")
        except:
            pass
