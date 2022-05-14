import discord, services
from discord.ext import commands
from NumberApi.number_api import NumberApi
from database import db
func = ["", "Number", "Time", "Service", "Server", "Status"]

class Number(commands.Cog, NumberApi):
    
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.data = {}
        
    
    @commands.command()
    @commands.is_owner()
    async def hist(self, ctx):
        history = await self.get_history()
        description = ""
        for i, data in enumerate(history):
            for index, target in enumerate(data):
                if target:
                    if index == 4: continue
                    if index == 5 and target != "REFUNDED": target = "OTP RECIEVED"
                    description += f"{func[index]} : {target.title()}\n"
            description += "=======================\n"
            if i == 19:
                break
        embed = discord.Embed(title = "__History of Numbers !__", description = description, color = discord.Colour.random())
        embed.set_footer(text = f"Requested by : {ctx.author}", icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = self.client.user.avatar_url)
        await ctx.send(embed = embed)
        
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
        response = await self.get_number(service.lower() if service.lower() not in ["mimir", "telegram", "fairplay"] else "others")
        error = response.get("error")
        if error:
            await ctx.send(ctx.author.mention + "\n```\n" + error + "\n```")
            return await self.client.get_channel(973629964056399882).send(error)
        number = response.get("number")
        activation_id = response.get("id")
        balance = response.get("balance")
        embed = discord.Embed(title = "__Number for {} !__".format(service.title()), color = discord.Colour.random())
        embed.add_field(name = "Number", value = number, inline = False)
        embed.add_field(name = "Activation ID", value = activation_id, inline = False)
        embed.set_thumbnail(url = self.client.user.avatar_url)
        embed.set_footer(text = "Requested by : {}".format(ctx.author), icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        self.data[activation_id] = {}
        self.data[activation_id]["sms"] = False
        self.data[activation_id]["price"] = price
        self.data[activation_id]["number"] = number
        embed = discord.Embed(title = "__Number Buyer Information !__", color = discord.Colour.random())
        embed.description = f"• Username : {ctx.author}\n• User ID : {ctx.author.id}\n• Service : {service.title()}\n• Number : {number}\n• Activation ID : {activation_id}\n• Remaining Balance : ₹{balance}\n"
        embed.set_thumbnail(url = self.client.user.avatar_url)
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
        number = self.data.get(activation_id).get("number")
        if sms:
            embed = discord.Embed(title = "__+91" + str(number) + "__", description = sms, color = discord.Colour.random())
            await ctx.send(embed = embed)
            embed = discord.Embed(title = "__Otp Status !__", description = f"Number : {number}\nActivation ID : {activation_id}\nStatus : Otp Recieved\nBalance : ₹{balance}\nPoints : {points-price} points", color = discord.Colour.random())
            embed.set_thumbnail(url = self.client.user.avatar_url)
            await self.client.get_channel(974325308251594814).send(embed = embed)
        else:
            embed = discord.Embed(title = "__+91" + str(number) + "__", description = "Didn't come any messages.", color = discord.Colour.random())
            await ctx.send(embed = embed)
            
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cancel(self, ctx, activation_id: int = None):
        if ctx.guild: return await ctx.send(ctx.author.mention + ", You can use this command only in DM!")
        if not activation_id: return await ctx.send(ctx.author.mention + ", You didn't enter activation ID!")
        response = await self.cancel_order(activation_id)
        error = response.get("error")
        if error: return await ctx.send(ctx.author.mention + "\n```\n" + error + "\n```")
        message = response.get("msg")
        points = db.user.find_one({"user_id": ctx.author.id}).get("points")
        balance, total_otp = await self.get_balance()
        await ctx.send(ctx.author.mention + ", " + message)
        number = self.data.get(activation_id).get("number")
        embed = discord.Embed(title = "__Otp Status !__", description = f"Number : {number}\nActivation ID : {activation_id}\nStatus : Cancelled\n{balance}rs\nPoints : {points} points", color = discord.Colour.random())
        embed.set_thumbnail(url = self.client.user.avatar_url)
        await self.client.get_channel(974325308251594814).send(embed = embed)
        
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
        embed.set_thumbnail(url = self.client.user.avatar_url)
        await ctx.send(embed = embed)
        
def setup(client):
    client.add_cog(Number(client))