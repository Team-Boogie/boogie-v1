import type_definitions
from mitmproxy.addonmanager import AddonManager
from .images import Images
from .lightswitch import LightSwitch

from .LockerV4.ActiveLoadoutGroup import ALG as ActiveLoadoutGroup
from .LockerV4.QueryItems import QI as QueryItems

from .Exploits.blurl_exploit import blurl
from .Exploits.lfg_exploit import lfg
from .Exploits.playlist_exploit import playlist
from .Exploits.name_exploit import name


def add_addons(
    user_settings: type_definitions.defaultUserSettings, addons: AddonManager
):
    #addons.add(CloudStorage(user_settings))
    addons.add(Images(user_settings))
    addons.add(LightSwitch(user_settings))
    addons.add(ActiveLoadoutGroup(user_settings))
    addons.add(QueryItems(user_settings))
    addons.add(blurl(user_settings))
    addons.add(lfg(user_settings))
    addons.add(playlist(user_settings))
    addons.add(name(user_settings))
