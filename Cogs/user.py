import discord
from discord.ext import commands
from database import db

class UserDetails(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["point"])
    async def points(self, ctx, member: discord.Member = None):
        if not member: member = ctx.author
        user = db.user.find_one({"user_id": member.id})
        if user:
            points = user.get("points")
        else:
            points = 0
        await ctx.send(member.mention + " has **{}** points!".format(points))
        
    @commands.command()
    async def give(self, ctx, amount: int = None, member: discord.Member = None):
        if not amount: return await ctx.send(ctx.author.mention + ", Please mention the amount to share your points.")
        if not member: return await ctx.send(ctx.author.mention + ", Please mention someone to share your points.")
        if member.bot: return await ctx.send(ctx.author.mention + ", You can't share your points to a bot user.")
        if member == ctx.author: return await ctx.send(ctx.author.mention + ", You can't share your points yourself.")
            
        
        
def setup(client):
    client.add_cog(UserDetails(client))