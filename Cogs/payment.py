import discord
from discord.ext import commands
from database import db

class UserDetails(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def buy(self, points: int = None):
        if not points: return await ctx.send(ctx.author.mention + ", You didn't enter any points amount.")
        