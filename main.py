import discord, asyncio
from discord.ext import commands
import os, sys, traceback

class MainClass(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready!")
        game = discord.Streaming(name = f"with >help | {str(len(self.client.guilds))} guilds", url = "https://app.mimirquiz.com")
        await self.client.change_presence(activity=game)
        
    @commands.command()
    async
    
    
intents = discord.Intents.all()
client = commands.Bot(command_prefix = "-", strip_after_prefix = True, case_insensitive = True, intents = intents)
client.remove_command("help")
client.add_cog(MainClass(client))

extensions = ["payment", "number", "user"]


if __name__ == "__main__":
    failed_ext = ""
    for extension in extensions:
        try:
            client.load_extension("Cogs."+extension)
        except Exception as e:
            failed_ext += f"{extension}, "
            print(f"Error loading {extension}", file=sys.stderr)
            traceback.print_exc()
    if failed_ext != "":
        print("Loaded Failed :", failed_ext)
    else:
        print("Extensions Loaded Successful!")