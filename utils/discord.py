import base64
import os
import urllib.parse
import hashlib

import aiohttp
import constants


def generate_code_verifier():
    return (
        base64.urlsafe_b64encode(os.urandom(32))
        .decode("utf-8")
        .replace("+", "")
        .replace("/", "")
        .replace("=", "")
    )


def create_authorization_url(code_challenge: str):
    return urllib.parse.urlunparse(
        (
            "https",
            "discord.com",
            "/oauth2/authorize",
            "",
            urllib.parse.urlencode(
                {
                    "response_type": "code",
                    "code_challenge": code_challenge,
                    "client_id": constants.CLIENT_ID,
                    "redirect_uri": "boogie://authorize",
                    "scope": "identify",
                }
            ),
            "",
        )
    )


def generate_code_challenge(code_verifier: str):
    return (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .decode("utf-8")
        .replace("=", "")
    )


async def exchange_for_tokens(
    session: aiohttp.ClientSession, code_verifier: str, authorization_code: str
) -> tuple[str, str]:
    async with session.post(
        "https://discord.com/api/oauth2/token",
        data={
            "grant_type": "authorization_code",
            "client_id": constants.CLIENT_ID,
            "code_verifier": code_verifier,
            "code": authorization_code,
            "redirect_uri": "boogie://authorize",
        },
    ) as resp:
        response = await resp.json()
    return response["access_token"], response["refresh_token"]


async def get_id(session: aiohttp.ClientSession, access_token: str) -> str:
    async with session.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"},
    ) as resp:
        return (await resp.json())["id"]


async def get_access_token(
    session: aiohttp.ClientSession, refresh_token: str
) -> tuple[str, str]:
    async with session.post(
        url="https://discord.com/api/oauth2/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        auth=aiohttp.BasicAuth(constants.CLIENT_ID, constants.CLIENT_SECRET),
    ) as resp:
        response = await resp.json()

    return response["access_token"], response["refresh_token"]
