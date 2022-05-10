import discord
from discord.ext import commands
from database import db

class UserDetails(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def buy(self, points: int = None):
        if ctx.guild: await ctx.send(ctx.author.mention + "**, Let's continue in DM!**")
        if not points: return await ctx.send(ctx.author.mention + ", You didn't enter any points amount.")
        embed = discord.Embed(title = "Payment Instructions !",
            description = "Please send exactly **₹{}** to the following QR! After payment send your Order ID or Transaction ID here within 5 minutes. Your points will be given within 10 minutes.".format(points),
            color = discord.Colour.random())
        embed.set_image(url = url)
        embed.set_footer(text = "Payment Created by : {}".format(ctx.author))