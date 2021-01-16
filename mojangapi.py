import aiohttp
import json
import base64


class KnownURIs:
    uuidURI = "https://api.mojang.com/users/profiles/minecraft/"
    MojangAccUUID = "https://api.mojang.com/user/profiles/"
    sessionServer = "https://sessionserver.mojang.com/session/minecraft/profile/"


async def perform_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            if res.status == 200:
                return await res.json()
            else:
                raise LookupError("LookupFailed")


async def get_uuid(playername):
    resp = await perform_request( KnownURIs.uuidURI + playername)
    return resp["id"]

async def get_profile(uuid, decode = False):
    resp =  await perform_request(KnownURIs.sessionServer + uuid)
    if decode:
        resp["properties"][0]["value"] = base64.b64decode(resp["properties"][0]["value"])
        return resp
    else:
        return resp

async def get_names(uuid):
    return await perform_request(KnownURIs.MojangAccUUID + uuid + "/names")