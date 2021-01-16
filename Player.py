import mojangapi
import base64;
import aiohttp

#OOP in Wrapper

class Player():

    """
    def create(username):
        self = Player()
        self.username= username
        self.uuid = None
        self.skinURI = None
        return self
    """
    def __init__(self, username):
        self.username= username
        self.uuid = None
        self.skinURI = None

    async def get_uuid(self):
        if self.uuid == None: #Caching
            resp = await mojangapi.perform_request( mojangapi.KnownURIs.uuidURI + self.username)
            self.uuid = resp["id"]
            return self.uuid
        else:
            return self.uuid

    async def get_profile(self,decode = False):
        uuid = await self.get_uuid()
        resp =  await mojangapi.perform_request(mojangapi.KnownURIs.sessionServer + uuid)
        if decode:
            resp["properties"][0]["value"] = base64.b64decode(resp["properties"][0]["value"])
            return resp
        else:
            return resp
    async def get_names(self):
        uuid = await self.get_uuid()
        return await mojangapi.perform_request(mojangapi.KnownURIs.MojangAccUUID + uuid + "/names")

    async def download_skin(self):
        async with aiohttp.ClientSession() as session:
            skin = await self.get_skin()
            async with session.get(skin) as res:
                if res.status == 200:
                
                    with open('download.png', 'wb') as file:
                        while True:
                            chunk = await res.content.read(500)
                            if not chunk:
                                print("Download finished!")
                                break
                            else:
                                file.write(chunk)
        
                else:
                    raise LookupError("LookupFailed")

    async def get_skin(self):
        if self.skinURI == None: #Caching
            uuid = await self.get_uuid()
            decoded = await self.get_profile(True)
            self.skinURI = eval(decoded["properties"][0]["value"].decode("ascii"))["textures"]["SKIN"]["url"]
        else:
            return self.skinURI
