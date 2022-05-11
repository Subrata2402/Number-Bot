import discord, services
from discord.ext import commands
from NumberApi.number_api import NumberApi
from database import db

class Number(commands.Cog, NumberApi):
    
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.data = {}
        
    @commands.command()
    @commands.is_owner()
    async def balance(self, ctx):
        balance, total_otp = await self.get_balance()
        embed = discord.Embed(title = total_otp + "\n" + balance + "rs", color = discord.Colour.random())
        await ctx.send(embed = embed)

    @commands.command(aliases = ["prices"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def price(self, ctx):
        description = ""
        embed = discord.Embed(title = "__Price list of Services !__", color = discord.Colour.random())
        for key, value in services.service_list.items():
            description += "• {} - {} points\n".format(key.title(), value)
        embed.description = "```\n{}\n```".format(description)
        embed.set_thumbnail(url = self.client.user.avatar_url)
        await ctx.send(embed = embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def getnumber(self, ctx, service: str = None):
        if ctx.guild: return await ctx.send(ctx.author.mention + ", You can use this command only in DM!")
        if not service: return await ctx.send(ctx.author.mention + ", Please provide a service name to request a number.")
        price = services.service_list.get(service.lower())
        if not price:
            return await ctx.send(ctx.author.mention + f", Invalid service name. Please use `{ctx.prefix}price` to get a list of services and their prices.")
        self_details = db.user.find_one({"user_id": ctx.author.id})
        if not self_details: return await ctx.send(ctx.author.mention + ", You don't have enough points to buy numb.")
        points = self_details.get("points")
        if points < price: return await ctx.send(ctx.author.mention + ", You don't have enough points to buy number.")
        response = await self.get_number(service.lower() if service.lower() not in ["mimir", "telegram"] else "others")
        error = response.get("error")
        if error:
            await ctx.send("Something went wrong please try again after some times.")
            return await self.client.get_channel(973629964056399882).send(error)
        number = response.get("number")
        activation_id = response.get("id")
        balance = response.get("balance")
        embed = discord.Embed(title = "Number for {}".format(service.title()), color = discord.Colour.random())
        embed.add_field(name = "Number", value = number, inline = False)
        embed.add_field(name = "Activation ID", value = activation_id, inline = False)
        embed.set_thumbnail(url = self.client.user.avatar_url)
        embed.set_footer(text = "Requested by : {}".format(ctx.author), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        self.data[activation_id] = {}
        self.data[activation_id]["sms"] = False
        self.data[activation_id]["price"] = price
        embed = discord.Embed(title = "Number Buyer Information !", color = discord.Colour.random())
        embed.description = f"• Username : {ctx.author}\n• User ID : {ctx.author.id}\n• Service : {service.title()}\n• Number : {number}\n• Activation ID : {activation_id}\n• Remaining Balance : ₹{balance}\n"
        await self.client.get_channel(973630743861415986).send(embed = embed)
        
    @commands.command(aliases = ["getcode"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def getsms(self, ctx, activation_id: int = None):
        if ctx.guild: return await ctx.send(ctx.author.mention + ", You can use this command only in DM!")
        if not activation_id: return await ctx.send(ctx.author.mention + ", You didn't enter activation ID!")
        response = await self.get_sms(activation_id)
        error = response.get("error")
        if error: return await ctx.send(ctx.author.mention + "\n```\n" + error + "\n```")
        sms = response.get("sms")
        balance = response.get("balance")
        check = self.data.get(activation_id).get("sms")
        if not check and sms:
            price = self.data.get(activation_id).get("price")
            points = db.user.find_one({"user_id": ctx.author.id}).get("points")
            update = {"points": points - price}
            db.user.update_one({"user_id": ctx.author.id}, {"$set": update})
            self.data[activation_id]["sms"] = True
        if sms:
            await ctx.send(ctx.author.mention + "\n```\n" + str(sms) + "\n```")
        else:
            await ctx.send(ctx.author.mention + "\n```\nDidn't come any messages yet.\n```")
            
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cancel(self, ctx, activation_id: int = None):
        if ctx.guild: return await ctx.send(ctx.author.mention + ", You can use this command only in DM!")
        if not activation_id: return await ctx.send(ctx.author.mention + ", You didn't enter activation ID!")
        response = await self.cancel_order(activation_id)
        error = response.get("error")
        if error: return await ctx.send(ctx.author.mention + "\n```\n" + error + "\n```")
        message = response.get("msg")
        await ctx.send(ctx.author.mention + ", " + message)
        
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def history(self, ctx, activation_id: int = None):
        if ctx.guild: return await ctx.send(ctx.author.mention + ", You can use this command only in DM!")
        if not activation_id: return await ctx.send(ctx.author.mention + ", You didn't enter activation ID!")
        response = await self.get_message_history(activation_id)
        error = response.get("error")
        if error: return await ctx.send(ctx.author.mention + "\n```\n" + error + "\n```")
        total_message = response.get("count")
        messages = response.get("sms")
        description = ""
        for message in messages:
            description += str(message) + "\n\n"
        embed = discord.Embed(title = "History of Messages !", description = description, color = discord.Colour.random())
        await ctx.send(embed = embed)
        
def setup(client):
    client.add_cog(Number(client))