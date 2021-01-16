import asyncio
import aiohttp
import mojangapi
from argparse import ArgumentParser

# Initialize argsparser
parser = ArgumentParser(description="Leverages Mojangs API -- Will execute only switch (in order of appearance)")
parser.add_argument("Username", help="Minecraft username")
parser.add_argument("--uuid", action="store_true", help="Prints uuid and exits")
parser.add_argument("--history", action="store_true", help="See account name history")
parser.add_argument("--session",action="store_true", help="Prints sessioninformation and exits")
parser.add_argument("--decode",action="store_true", help="decode base64 encrypted contents")
parser.add_argument("--skin", action="store_true", help="Download skin to current folder")
args=parser.parse_args()
#EO argsparser
# Downloader
async def perform_download(url):
    async def request():
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                if res.status == 200:
             
                    with open('download.png', 'wb') as file:
                        while True:
                            chunk = await res.content.read(500)
                            if not chunk:
                                break
                            else:
                                file.write(chunk)
    
                else:
                    raise LookupError("LookupFailed")
    await request()
  
# EO Downloader

async def main():
    if args.Username != None:
        if args.uuid:
            uuid = await mojangapi.get_uuid(args.Username)
            print(uuid)
            return
        if args.session:
            uuid = await mojangapi.get_uuid(args.Username)
            session = await mojangapi.get_profile(uuid,args.decode)
            print(session)
            return
        if args.skin:
           uuid = await mojangapi.get_uuid(args.Username)
           decoded = await  mojangapi.get_profile(uuid, True)
           stringified = eval(decoded["properties"][0]["value"].decode("ascii"))["textures"]["SKIN"]["url"]
           await perform_download(stringified)
           return
        if args.history:
            uuid = await mojangapi.get_uuid(args.Username)
            history = await mojangapi.get_names(uuid)
            print(history)
            return
        else:
            print("Please use -h switch")
    else:
        print("Please enter a valid username!")

asyncio.run(main())