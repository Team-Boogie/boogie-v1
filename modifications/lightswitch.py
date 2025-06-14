import json

from mitmproxy import http

from type_definitions import defaultUserSettings, LightswitchService
from utils import checks
from urllib import parse


class LightSwitch:
    def __init__(self, userSettings: defaultUserSettings):
        self.userSettings: defaultUserSettings = userSettings

    @checks.is_fortnite_request
    def request(self, flow: http.HTTPFlow):
        url = parse.urlparse(flow.request.url)

        if (
            url.path != "/lightswitch/api/service/bulk/status"
        ):  # https://github.com/LeleDerGrasshalmi/FortniteEndpointsDocumentation/tree/main/EpicGames/LightswitchService
            return

        if parse.parse_qs(url.query)["serviceId"][0] != "Fortnite":
            return

        status: list[LightswitchService] = [
            {
                "serviceInstanceId": "fortnite",
                "status": "UP",
                "message": "Fortnite is online",
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

        flow.response = http.Response.make(
            200, json.dumps(status), http.Headers(content_type="application/json")
        )
