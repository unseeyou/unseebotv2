import io
import asyncio
import random
import os
import discord
import aiohttp
import time
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from typing import Literal

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
# bot = commands.Bot(command_prefix='t!', case_insensitive=True, intents=intents, help_command=None)
bot = commands.Bot(command_prefix='t!', help_command=None, case_insensitive=True, intents=intents, activity=discord.Game('With your mind - >help'), status=discord.Status.online)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

splash_text = """
██╗░░░██╗███╗░░██╗░██████╗███████╗███████╗██████╗░░█████╗░████████╗
██║░░░██║████╗░██║██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗╚══██╔══╝
██║░░░██║██╔██╗██║╚█████╗░█████╗░░█████╗░░██████╦╝██║░░██║░░░██║░░░
██║░░░██║██║╚████║░╚═══██╗██╔══╝░░██╔══╝░░██╔══██╗██║░░██║░░░██║░░░
╚██████╔╝██║░╚███║██████╔╝███████╗███████╗██████╦╝╚█████╔╝░░░██║░░░
░╚═════╝░╚═╝░░╚══╝╚═════╝░╚══════╝╚══════╝╚═════╝░░╚════╝░░░░╚═╝░░░"""


@bot.event
async def on_ready():
    # now start the bot
    print(splash_text)
    # await bot.change_presence(activity=discord.Game('With your mind - t!help'), status=discord.Status.online)
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=applications.commands%20bot")
    print('------')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, this command does not exist. Contact unseeyou#2912 if you think this should be added.")


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


@bot.tree.command(name="say", description="say things")
async def _say(interaction: discord.Interaction, string: str):
    await interaction.response.send_message(string)


@bot.command(pass_context=True)
async def unseebot(ctx):
    await ctx.send('Check your dms!')
    await ctx.message.author.send(
        "Hi! I'm unseebot, a bot made by unseeyou. Please feel free to report any issues to unseeyou via dms. Thanks!")


@bot.command()  # clear command
@commands.has_permissions(manage_messages=True)
async def clear(ctx, quantity: int):
    await ctx.send(f"clearing {quantity} messages")
    channel = ctx.channel
    await channel.purge(limit=int(quantity) + 1)  # clears command usage as well as amount of messages
    msg = await ctx.send(f"cleared {quantity} messages!")
    time.sleep(2)
    await msg.delete()


@bot.hybrid_command()
async def yt(ctx):
    try:
        link = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        await ctx.send(f"Click on the blue link to start the event!\n{link}")
    except Exception as err:
        print(err)
        await ctx.send(err)


@bot.hybrid_command(aliases=['doggo', 'dogs', 'dogfacts', 'dogfact', 'pup', 'pupper', 'puppy'])
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')
        dogjson = await request.json()
        request2 = await session.get('https://some-random-api.ml/facts/dog')
        factjson = await request2.json()
    dogbed = discord.Embed(title='DOGGY', colour=discord.Colour.dark_gold())
    dogbed.set_image(url=dogjson['link'])
    dogbed.set_footer(text=factjson['fact'])
    await ctx.send(embed=dogbed)


@bot.command()
async def anal(ctx):
    await ctx.send('https://tenor.com/view/sheep-anal-sheep-bum-bum-stab-from-behind-gif-19411863')


@bot.hybrid_command(aliases=['kitty', 'kitten', 'meow', 'catfact', 'catfacts'])
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        request1 = await session.get('https://some-random-api.ml/img/cat')
        catjson = await request1.json()
        request22 = await session.get('https://some-random-api.ml/facts/cat')
        factjson1 = await request22.json()
    catty = discord.Embed(title='KITTY', colour=discord.Colour.dark_gold())
    catty.set_image(url=catjson['link'])
    catty.set_footer(text=factjson1['fact'])
    await ctx.send(embed=catty)


@bot.command(pass_context=True)
async def id(ctx):
    id = ctx.message.guild.id
    await ctx.send(id)


@bot.hybrid_command()
async def poker(ctx):
    try:
        invite = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'poker')
        await ctx.send(f'click on this link to start the game!\n{invite}')
    except Exception as err:
        print(err)
        await ctx.send(err)


@bot.hybrid_command(aliases=['draw', 'skribbl', 'scribble', 'skribbl.io'])
async def doodle(ctx):
    try:
        invite = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'sketch-heads')
        await ctx.send(f'click on this link to start the game!\n{invite}')
    except Exception as err:
        print(err)
        await ctx.send(err)


@bot.hybrid_command()
async def word(ctx):
    try:
        invite = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'awkword')
        await ctx.send(f'click on this link to start the game!\n{invite}')
    except Exception as err:
        print(err)
        await ctx.send(err)


@bot.hybrid_command()
async def golf(ctx):
    try:
        invite = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'putt-party')
        await ctx.send(f'click on this link to start the game!\n{invite}')
    except Exception as err:
        print(err)
        await ctx.send(err)


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


@bot.hybrid_command()
async def hello(ctx):
    await ctx.send('Hello!')


@bot.command()
async def sudo(ctx, member: discord.Member, *, message=None):
    await ctx.message.delete()
    if message is None:
        await ctx.send(f'SyntaxError: a person and message must be specified')
        return

    webhook = await ctx.channel.create_webhook(name=member.name)
    await webhook.send(
        str(message), username=member.nick, avatar_url=member.avatar)

    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
        await webhook.delete()


@bot.hybrid_command()
async def echo(ctx, *, message: str):
    try:
        await ctx.message.delete()
    except Exception:
        pass
    await ctx.send(message)


@bot.hybrid_command(name='8ball')
async def _8ball(ctx, message: str):
    if message:
        # print(message)
        ans = ['my sources say yes', 'hell no', 'ask again later', "idk man you're on your own", 'sure, why not?',
               'how about... no?']
        await ctx.reply(random.choice(ans))
    else:
        await ctx.reply('ask me a question')  # TODO: fix this message not sending
        # attempt 1: replacing if/else with try/except


@bot.hybrid_command()
async def invite(ctx):
    embed = discord.Embed(title='click here', description='to invite unseebot to your server',
                          url='https://discord.com/api/oauth2/authorize?client_id=915182238239449099&permissions=8&scope=bot%20applications.commands')
    await ctx.send(embed=embed)


@bot.hybrid_command()
async def github(ctx):
    git = discord.Embed(title='link', url='https://github.com/unseeyou/unseebot',
                        description="click on the link to open unseebot's github page",
                        colour=discord.Colour.dark_gray())
    git.set_image(
        url='https://images-ext-2.discordapp.net/external/pe2rnxtS-petcef7jYVHtm1ncabRKulTvDV70G1F5O8/https/repository-images.githubusercontent.com/435063686/e6f3942e-98dd-407b-9fbc-4ba1dbe89849')
    await ctx.send(embed=git)


@bot.tree.command(description='Says hello!')
async def hi(interaction: discord.Interaction):  # slash command!
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


@bot.hybrid_command(help='probably my ping')
async def ping(ctx: commands.Context):
    latency = round(bot.latency*1000, 2)
    message = await ctx.send("Pong!")
    await message.edit(content=f"Pong! My ping is `{latency} ms`")
    print(f'Ping: `{latency} ms`')


@bot.tree.command()
@app_commands.describe(action='The action to do in the shop', item='The target item')
async def shop(interaction: discord.Interaction, action: Literal['Buy', 'Sell'], item: str):
    """Interact with the shop"""
    await interaction.response.send_message(f'Action: {action}\nItem: {item}')


async def main():
    async with bot:
        # first load the general cogs
        print('loading cogs...')
        cogs = ['epic', 'fakehack', 'help', 'hystats', 'meme', 'numbergame', 'poll', 'pplength',
                'tictactoe', 'tts', 'twitch', 'urban', 'xkcd', 'music', 'pfp-gg', 'nim_game', 'profile-filters']
        for cog in cogs:
            print(f"loading {cog}")
            await bot.load_extension(f"cogs.{cog}")
            print(f'loaded {cog}')

        # now load the utils
        await bot.load_extension("utils.log")
        await bot.load_extension("utils.controls")
        await bot.load_extension("web_panel.test")

        print('now actually starting the bot...')
        await bot.start(TOKEN)


asyncio.run(main())
