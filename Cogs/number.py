import discord, services
from discord.ext import commands
from NumberApi.number_api import NumberApi
from database import db

class Number(commands.Cog, NumberApi):
    
    def __init__(self, client):
        super().__init__()
        self.client = client

    @commands.command()
    async def get(self, service: str = None):
        if not service: return await ctx.send("Please provide a service name to request a number.")
        price = services.get(service.lower())
        if not price:
            return await ctx.send(f"Invalid service name. Please use `{ctx.prefix}price` to get a list of price of service.")
        