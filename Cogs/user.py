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
        self_details = db.user.find_one({"user_id": ctx.author.id})
        if not self.self_details: return await ctx.send(ctx.author.mention + ", You don't have any points to share. To buy points use Command `{}buy`!".format(ctx.prefix))
        self_points = self_details.get("points")
        if self_points < amount: return await ctx.send(ctx.author.mention + ", You don't have enough points to share **{}** points. To buy points use command `{}buy`!".format(amount, ctx.prefix))
        user_details = db.user.find_one({"user_id": member.id})
        if not user_details:
            db.user.insert_one({"user_id": member.id, "points": amount})
        else:
            user_points = user_details.get("points")
            user_update = {"points": user_points + amount}
            db.user.update_one({"user_id": member.id}, {"$set": user_update})
        self_update = {"points": self_points - amount}
        db.user.update_one({"user_id": ctx.author.id}, {"$set": self_update})
        await ctx.send(ctx.author.mention + ", You gave **{}** points to {}!".format(amount, member.mention))
        
def setup(client):
    client.add_cog(UserDetails(client))