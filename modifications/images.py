from mitmproxy import http

from type_definitions import defaultUserSettings
from utils import config
from constants import URLs
from urllib import parse
from utils import checks


class Images:
    def __init__(self, userSettings: defaultUserSettings):
        self.userSettings: defaultUserSettings = userSettings


    @checks.is_fortnite_request
    def request(self, flow: http.HTTPFlow):
        path = parse.urlparse(flow.request.url).path

        if (
            not path.endswith(".png")
            and not path.endswith(".jpg")
            and not path.endswith(".jpeg")
        ):  # exits if it's not an image
            return

        if (
            self.userSettings["premium"]
            and not config.read()["extraSettings"]["images_enabled"]
        ):  # exits if user has premium and they have image replacements disabled
            return

        flow.request.url = (
            f"{URLs.CDN}/SplashScreen.png"
            if not self.userSettings["premium"]
            else config.read()["extraSettings"]["image"]
        )
