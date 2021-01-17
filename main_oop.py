import asyncio
import aiohttp
import mojangapi
import Player
from argparse import ArgumentParser

# Initialize argsparser
parser = ArgumentParser(description="Leverages Mojangs API -- Will execute only one (except for '--decode' alongside with '--session') switch (in order of appearance)")
parser.add_argument("Username", help="Minecraft username")
parser.add_argument("--uuid", action="store_true", help="Prints uuid and exits")
parser.add_argument("--history", action="store_true", help="See account name history")
parser.add_argument("--session",action="store_true", help="Prints sessioninformation and exits")
parser.add_argument("--decode",action="store_true", help="decode base64 encrypted contents")
parser.add_argument("--skin", action="store_true", help="Download skin to current folder")
args=parser.parse_args()
#EO argsparser


async def main():
    if args.Username != None:
            myPlayer = Player.Player(args.Username)
            if args.uuid:
                print(await myPlayer.get_uuid())
                return
            if args.session:
                print(await myPlayer.get_profile(args.decode))
                return
            if args.skin:
                await myPlayer.download_skin()
                return
            if args.history:
                print(await myPlayer.get_names())
                return
            else:
                print("Please use -h switch")
    else:
        print("Please enter a valid username!")

asyncio.run(main())