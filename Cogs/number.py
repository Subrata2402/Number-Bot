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
        if ctx.guild: return await ctx.send(ctx.author.mention + ", You can use this command only in DM!"
        if not service: return await ctx.send(ctx.author.mention + ", Please provide a service name to request a number.")
        price = services.service_list.get(service.lower())
        if not price:
            return await ctx.send(ctx.author.mention + f", Invalid service name. Please use `{ctx.prefix}price` to get a list of price of service.")
        self_details = db.user.find_one({"user_id": ctx.author.id})
        if not self_details: return await ctx.send(ctx.author.mention + ", You don't have enough points to buy numb.")
        points = self_details.get("points")
        if points < price: return await ctx.send(ctx.author.mention + ", You don't have enough points to buy number.")
        response = await self.get_number(service.lower())
        error = response.get("error")
        if error:
            await ctx.send("Something went wrong please try again after some times.")
            return await self.client.get_channel(973629964056399882).send(error)
        number = response.get("number")
        activation_id = response.get("activation_id")
        balance = response.get("balance")
        embed = discord.Embed(title = "Number for {}".format(service.title()), color = discord.Colour.random(),
        embed.add_field(name = "Number", value = number, inline = False)
        embed.add_field(name = "Activation ID", value = activation_id, inline = False)
        embed.set_thumbnail(url = self.client.user.avatar_url)
        embed.set_footer(text = "Requested by : {}".format(ctx.author), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        embed = discord.Embed(title = "Number Buyer Information !", color = discord.Colour.random())
        embed.description = f"• Username : {ctx.author}\n• User ID : {ctx.author.id}\n• Number : {number}\n• Activation ID : {activation_id}\n• Remaining Balance : {balance}\n"
        await self.client.get_channel(973630743861415986).send(embed = embed)
        
def setup(client):
    client.add_cog(Number(client))