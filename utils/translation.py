import aiohttp
import constants
from . import config
import type_definitions

translations: type_definitions.TranslationsFile | None = None


async def init_translations(session: aiohttp.ClientSession):
    global translations
    async with session.get(f"{constants.URLs.CDN}/translations.json") as resp:
        translations = await resp.json()


def get(key: str):
    assert translations is not None
    finals = translations["translations"]
    text = finals[key]
    language: str = config.read()["extraSettings"]["lang"]
    if text.get(language.lower()):
        return text[language.lower()]
    else:
        return text["en"]


def avaliable(language: str):
    assert translations is not None
    if language.lower() in translations["aliases"]:
        return True
    else:
        return False


def contributors():
    assert translations is not None
    return translations["contritbutors"]
