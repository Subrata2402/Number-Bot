import discord
from discord.ext import commands
from database import db

class Payment(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def buy(self, ctx, points: int = None):
        if not points: return await ctx.send(ctx.author.mention + ", You didn't enter any points amount.")
        if ctx.guild: await ctx.send(ctx.author.mention + "**, Let's continue in DM!**")
        embed = discord.Embed(title = "Payment Instructions !",
            description = "Please send exactly **₹{}** to the following QR! After payment send your Order ID or Transaction ID here within 5 minutes. Your points will be given within 10 minutes.".format(points),
            color = discord.Colour.random())
        embed.set_image(url = "https://media.discordapp.net/attachments/860116826159316992/973671108421230612/IMG_20220511_010823.jpg")
        embed.set_footer(text = "Payment Created by : {}".format(ctx.author))
        await ctx.author.send(embed = embed)
        try:
            message = await self.client.wait_for("message", timeout = 300.0)
        except:
            return await ctx.author.send(ctx.author.mention + ", You failed to send your order ID within time. Don't worry if already paid the amount then start this session again and send your ID.")
        try:
            id = int(message.strip())
        except:
            return await ctx.author.send(ctx.author.mention + ", Invalid Order ID!")
            
        channel = self.client.get_channel(973640257612431401)
        embed = discord.Embed(title = "Payment Information !",
            description = f"```\n" \
                f"Username : {ctx.author}\n" \
                f"User ID : {ctx.author.id}\n" \
                f"Points Amount : {points}\n" \
                f"Order ID : {id}\n```",
            color = discord.Colour.random())
        await channel.send(embed = embed)
        
def setup(client):
    client.add_cog(Payment(client))