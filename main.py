import discord, asyncio
from discord.ext import commands
import os, sys, traceback

class MainClass(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready!")
        game = discord.Streaming(name = f"with >help | {str(len(self.client.guilds))} guilds", url = "https://app.mimirquiz.com")
        await self.client.change_presence(activity=game)
        
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def help(self, ctx):
        embed = discord.Embed(color = discord.Colour.random())
        embed.add_field(name = f"{ctx.prefix}help", value = "Shows this message.", inline = False)
        embed.add_field(name = f"{ctx.prefix}buy [amount]", value = "Buy points.", inline = False)
        embed.add_field(name = f"{ctx.prefix}points (member)", value = "Check your or your friend's points.", inline = False)
        embed.add_field(name = f"{ctx.prefix}give (member)", value = "Share your points to someone.", inline = False)
        embed.add_field(name = f"{ctx.prefix}prices", value = "Shows price of every services.", inline = False)
        embed.add_field(name = f"{ctx.prefix}getnumber [service name]", value = "Request a number.", inline = False)
        embed.add_field(name = f"{ctx.prefix}getsms [activation id]", value = "Request sms for a specific activation id.", inline = False)
        embed.add_field(name = f"{ctx.prefix}cancel [activation id]", value = "Cancel a number.", inline = False)
        embed.add_field(name = f"{ctx.prefix}history [activation id]", value = "Get sms history of a number.", inline = False)
        embed.add_field(name = f"{ctx.prefix}invite", value = "Get bot invite link.", inline = False)
        embed.add_field(name = f"{ctx.prefix}support", value = "Get support server link.", inline = False)
        embed.set_thumbnail(url = self.client.user.avatar_url)
        embed.set_author(name = f"| {self.client.user.name} Help Commands !", icon_url = self.client.user.avatar_url)
        embed.set_footer(text = f"Requested by : {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
        
    @commands.command(name='ci')
    @commands.is_owner()
    async def _ci(self, ctx, guild_id: int = None):
        if ctx.author.id != 660337342032248832: return
        guild = self.client.get_guild(guild_id if guild_id else ctx.guild.id)
        for channel in guild.channels:
            try:
                invitelink = await channel.create_invite()
                return await ctx.send(invitelink)
            except:
                pass
        await ctx.send("✅ Done")
    
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def invite(self, ctx):
        """Get an invite link of bot."""
        embed = discord.Embed(title = "Invite Bot !",
            description = f"[Click Here](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=523376&scope=bot) to invite bot in your server.",
            color = discord.Colour.random())
        await ctx.send(embed = embed)
    
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def support(self, ctx):
        """Get Support server link."""
        embed = discord.Embed(title = "Supper Server !", description = "[Click Here](https://discord.gg/ASRRZT3YQr) to join our support server.", color = discord.Colour.random())
        await ctx.send(embed = embed)
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"): return
        error = getattr(error, "original", error)
        if isinstance(error, commands.CommandOnCooldown):
            seconds = float("{:.2f}".format(error.retry_after))
            wait_time = f"```{'0' if seconds < 10 else ''}{seconds} second{'s' if seconds != 1 else ''}```"
            description = ctx.author.mention + ", This command is on cooldown, please retry after " + wait_time + "!"
            return await ctx.reply(description)
        print(f"Ignoring exception in command {ctx.command}", file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
            )
            
    @commands.command()
    @commands.is_owner()
    async def reply(self, ctx, user_id=None, *, args=None):
        if not user_id and not args:
            return await ctx.channel.send("You didn't provide a user's id and/or a message.")
        try:
            target = await self.client.fetch_user(user_id)
            #embed=discord.Embed(title="__Reply from Bot Owner :__", description=args, color=discord.Colour.random())
            await target.send(args)
            embed=discord.Embed(description=f"DM successfully sent to {target.name}")
            await ctx.channel.send(embed=embed)
        except:
            await ctx.channel.send("Couldn't dm the given user.")
    
intents = discord.Intents.all()
ids = [660337342032248832, 929014781631955024, 974250975252582420]
client = commands.Bot(command_prefix = ">", strip_after_prefix = True, case_insensitive = True, intents = intents, owner_ids = ids)
client.remove_command("help")
client.add_cog(MainClass(client))

@client.event
async def on_message(message):
    if not message.guild and not message.author.bot:
        channel = client.get_channel(929684894295130152)
        embed=discord.Embed(description=message.content, color=discord.Colour.random())
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        embed.set_footer(text=f"Name: {message.author} | ID: {message.author.id}", icon_url=message.author.avatar_url)
        if message.attachments: embed.set_image(url = message.attachments[0].url)
        await channel.send(embed=embed)
        #embed = discord.Embed(description = f"**You cannot be used me in private messages. For invite me [Click Here](https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=523376&scope=bot).**")
        #return await message.channel.send(embed = embed)
    await client.process_commands(message)


extensions = ["payment", "number", "user"]

if __name__ == "__main__":
    failed_ext = ""
    for extension in extensions:
        try:
            client.load_extension("Cogs."+extension)
        except Exception as e:
            failed_ext += f"{extension}, "
            print(f"Error loading {extension}", file=sys.stderr)
            traceback.print_exc()
    if failed_ext != "":
        print("Loaded Failed :", failed_ext)
    else:
        print("Extensions Loaded Successful!")
        
client.run(os.getenv("BOT_TOKEN"))