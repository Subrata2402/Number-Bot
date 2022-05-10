import discord, services
from discord.ext import commands
from NumberApi.number_api import NumberApi
from database import db

class Number(commands.Cog, NumberApi):
    
    def __init__(self, client):
        super().__init__()
        self.client = client

    @commands.command(aliases = ["prices"])
    async def price(self, ctx):
        description = ""
        embed = discord.Embed(title = "Price list of Services !", color = discord.Colour.random())
        for key, value in services.service_list:
            description += "• {} - ₹{}".format(key, value)
        embed.description = "```\n{}\n```".format(description)
        await ctx.send(embed = embed)
        

    @commands.command()
    async def getnumber(self, ctx, service: str = None):
        if not service: return await ctx.send(ctx.author.mention + ", Please provide a service name to request a number.")
        price = services.service_list.get(service.lower())
        if not price:
            return await ctx.send(ctx.author.mention + f", Invalid service name. Please use `{ctx.prefix}price` to get a list of price of service.")
        self_details = db.user.find_one({"user_id": ctx.author.id})
        if not self_details: return 
        
        
def setup(client):
    client.add_cog(Number(client))