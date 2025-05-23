__author__ = 'unseeyou'

import random
import os
import io
import discord
import aiohttp
import asyncio
import traceback
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix='>',
    help_command=None,
    case_insensitive=True,
    intents=intents,
    activity=discord.Game('With your mind'),
    status=discord.Status.online
)

load_dotenv()
TOKEN = os.getenv("UNSEEBOT_TOKEN")


async def activity_warn(ctx):
    await ctx.send("this is either because the server does not have activities enabled or you don't have nitro.")


@bot.event
async def on_ready():
    print(f'Logged in/Rejoined as {bot.user} (ID: {bot.user.id})')
    print(f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=applications.commands%20bot")
    print('------ Error Log ------')
    print(len(bot.users))


@bot.event
async def setup_hook():
    print('loading slash commands...')
    try:
        await bot.tree.sync(guild=None)
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
    print("If you are seeing this then unseeyou's epic bot is working!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, this command does not exist. Contact unseeyou#2912 if you think this should be added.")
    elif isinstance(error, discord.errors.NotFound):
        pass


@bot.listen()
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="join-leave")
    if channel is not None:
        embed = discord.Embed(color=0x4a3d9a)
        embed.add_field(name="Welcome", value=f"{member.mention} has joined {member.guild.name}", inline=False)
        await channel.send(embed=embed)
    else:
        pass


@bot.listen()
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name="join-leave")
    if channel is not None:
        embed = discord.Embed(color=0x4a3d9a)
        embed.add_field(name="Goodbye", value=f"{member.mention} has left {member.guild.name}", inline=False)
        await channel.send(embed=embed)
    else:
        pass


@bot.command(pass_context=True)
async def unseebot(ctx):
    await ctx.send('Check your dms!')
    await ctx.message.author.send(
        "Hi! I'm unseebot, a bot made by unseeyou. Please feel free to report any issues to unseeyou via dms. Thanks!")


@bot.hybrid_command(help='launches the youtube watch together discord activity if you are in a vc')
async def yt(ctx):
    try:
        link = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        await ctx.send(f"Click on the blue link to start the event!\n{link}")
    except Exception as err:
        print(err)
        await ctx.send(err)
        await activity_warn(ctx)


@bot.command()
async def anal(ctx):
    await ctx.send('https://tenor.com/view/sheep-anal-sheep-bum-bum-stab-from-behind-gif-19411863')


@bot.command(pass_context=True)
async def id(ctx):
    id = ctx.message.guild.id
    await ctx.send(id)


@bot.command()
async def bwstats(ctx, message=None):
    embed1 = discord.Embed(title='Hypixel Bedwars Statistics', url='https://bwstats.shivam.pro',
                           description='click the link to view stats', colour=discord.Colour.dark_gold())
    embed2 = discord.Embed(title='Hypixel Bedwars Statistics', url=f'https://bwstats.shivam.pro/user/{message}',
                           description=f'click the link to view the stats of {message}',
                           colour=discord.Colour.dark_gold())

    if message is None:
        await ctx.send(embed=embed1)
    else:
        await ctx.send(embed=embed2)


@bot.command()
async def sudo(ctx, member: discord.Member, *, message=None):
    await ctx.message.delete()
    if message is None:
        await ctx.send(f'SyntaxError: a person and message must be specified')
        return

    webhook: discord.Webhook = await ctx.channel.create_webhook(name=member.display_name)
    await webhook.send(
        str(message), username=member.display_name, avatar_url=member.display_avatar)
    await webhook.delete()


@bot.hybrid_command(help='repeats your message')
async def echo(ctx, *, message: str):
    try:
        await ctx.message.delete()
    except Exception:
        pass
    await ctx.send(message)


@bot.hybrid_command(name='8ball', help='classic 8ball. or is it?')
async def _8ball(ctx, message: str):
    if message is not None or False:
        ans = ['my sources say yes', 'hell no', 'ask again later', "idk man you're on your own", 'sure, why not?',
               'how about... no?']
        await ctx.reply(random.choice(ans))
    else:
        await ctx.reply('ask me a question')  # TODO: fix issue where this message isn't sending


@bot.hybrid_command(help='generates an invite link for unseebot. please use this and not my profile.')
async def invite(ctx):
    embed = discord.Embed(title='click here', description='to invite unseebot to your server',
                          url='https://discord.com/api/oauth2/authorize?client_id=915182238239449099&permissions=8&scope=bot%20applications.commands')
    await ctx.send(embed=embed)


@bot.hybrid_command(help='my github!')
async def github(ctx):
    git = discord.Embed(title='link', url='https://github.com/unseeyou/unseebot',
                        description="click on the link to open unseebot's github page",
                        colour=discord.Colour.dark_gray())
    git.set_image(
        url='https://images-ext-2.discordapp.net/external/pe2rnxtS-petcef7jYVHtm1ncabRKulTvDV70G1F5O8/https/repository-images.githubusercontent.com/435063686/e6f3942e-98dd-407b-9fbc-4ba1dbe89849')
    await ctx.send(embed=git)


@bot.hybrid_command(help='probably my ping')
async def ping(ctx: commands.Context):
    latency = round(bot.latency*1000, 2)
    message = await ctx.send("Pong!")
    await message.edit(content=f"Pong! My ping is `{latency} ms`")
    print(f'Ping: `{latency} ms`')


async def main():
    async with bot:
        cogs = ['epic', 'fakehack', 'hystats', 'numbergame', 'nim_game', 'poll', 'pplength',
                'tictactoe', 'tts', 'twitch', 'urban', 'xkcd', 'music', 'pfp-gg', 'profile-filters']
        for cog in cogs:
            print(f"loading {cog}")
            await bot.load_extension(f"cogs.{cog}")
            print(f'loaded {cog}')
        # load utils - same as cog but different directory
        await bot.load_extension("utils.log")
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
