import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
import os
import asyncio
import time
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=";", case_insensitive=True, intents=intents)
TOKEN = os.getenv('MODBOT_TOKEN')


@bot.event
async def on_ready():
    print('MODERATION BOT ONLINE')
    print(f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=applications.commands%20bot")


@bot.event
async def setup_hook():
    print('loading slash commands')
    await bot.tree.sync()


@bot.event
async def on_member_join(member):
    try:
        r = discord.utils.get(member.guild.roles, name='member')
        await member.add_roles(r)
    except Exception:
        pass



@bot.event
async def on_message(message):
    if message.channel.id == 1030228711993253988:
        await message.publish()
    else:
        await bot.process_commands(message)
        pass


@bot.command(aliases=['bc'], help='still working on it')
@commands.has_permissions(administrator=True)
async def broadcast(ctx, *, message=None):
    channels = ctx.guild.text_channels
    for channel in channels:
        await channel.send(f'**Server Broadcast:** {message}')


@bot.hybrid_command(help='run this if mute role isnt working')
@commands.has_permissions(administrator=True)
async def setupmute(ctx):
    msg = await ctx.send('`this may take a while if you have lots of text channels...`')
    muted_role = discord.utils.get(ctx.guild.roles, name="muted")
    for channel in ctx.guild.text_channels:
        await channel.set_permissions(muted_role, send_messages=False)
    embed = discord.Embed(title='COMPLETED!', colour=discord.Colour.green())
    await msg.delete()
    await ctx.reply(embed=embed)


@bot.command(help='usage: `sudo @mention {message}`')
@commands.has_permissions(administrator=True)
async def sudo(ctx, member: discord.Member, *, message: str = None):
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


@bot.hybrid_command(help='gets the current ping of bot')
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong! My ping is `{int(ping)}ms`")
    print(f'Ping: {int(ping)} ms')
    await message.reply('lol', mention_author=False)


@bot.hybrid_command(pass_context=True, help='gets the server/guild ID')
@commands.has_permissions(administrator=True)
async def id(ctx):
    id = ctx.message.guild.id
    await ctx.send(id)


@bot.hybrid_command(name='clear', aliases=['purge', 'delete', 'del'],
                    help='usage: `clear {quantity}`')  # clear command
@commands.has_permissions(administrator=True)
async def clear(ctx, quantity: int):
    await ctx.send(f"clearing {quantity} messages")
    channel = ctx.channel
    await channel.purge(limit=int(quantity) + 2)  # clears command usage as well as amount of messages
    time.sleep(0.2)
    msg = await ctx.send(f"cleared {quantity} messages!")
    msg2 = await ctx.send("just a reminder that this bot cannot delete messages more then 2 weeks old")
    time.sleep(2)
    await msg.delete()
    await msg2.delete()


@bot.hybrid_command(help='gives a role', aliases=['giverole'])
@commands.has_permissions(administrator=True)
async def role(ctx, member: discord.Member = None, role: discord.Role = None):
    if member is None:
        member = ctx.message.author
    else:
        pass
    role = discord.utils.get(ctx.guild.roles, name=role.name)
    await member.add_roles(role)


@bot.command(help='totally not sussy!!!')
@commands.has_permissions(administrator=True)
async def roleall(ctx, role: discord.Role):
    members = ctx.guild.members
    for member in members:
        await member.add_roles(role)


@bot.command(help='the ultimate undo')
@commands.has_permissions(administrator=True)
async def undoroleall(ctx, role: discord.Role):
    members = ctx.guild.members
    for user in members:
        if 'unseeyou' in user.username:
            pass
        else:
            await user.remove_roles(role)


@bot.hybrid_command(aliases=['rr'], help='trololol')
@commands.has_permissions(administrator=True)
async def removerole(ctx, role: discord.Role, user: discord.Member = None):
    if user is None:
        user = ctx.message.author
    else:
        pass
    await user.remove_roles(role)


@bot.hybrid_command(help='locks down a channel, only admins can talk and unlock it', aliases=['lock', 'ld'])
@commands.has_permissions(administrator=True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(ctx.channel.mention + " ***is now in lockdown.***")


@bot.hybrid_command(help='unlocks a channel', aliases=['unlockdown', 'uld', 'ul'])
@commands.has_permissions(administrator=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***has been unlocked.***")


@bot.command(help='changes all the nicknames')
@commands.has_permissions(administrator=True)
async def nickall(ctx, *, nick='[insert nick here]'):
    for user in ctx.guild.members:
        try:
            await user.edit(nick=nick)
        except discord.Forbidden:
            pass


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(error)
        await ctx.send(error)


@bot.command(help='B I G   R E D   B U T T O N')
async def button(ctx):
    view = View()
    embed = discord.Embed(title='USE WITH CAUTION', colour=discord.Colour.red())
    embed.set_author(icon_url=ctx.author.avatar.url, name=f"sent by {ctx.author.name}")

    async def callback(interaction):
        if ctx.message.author.id == 650923352097292299:
            pass
            # await interaction.response.send_message('__**SERVER WILL GO BOOM BOOM IN 30 SECONDS**__')
        else:
            await interaction.response.send_message('`Error 69420: you are not unseeyou`', ephemeral=True)

    button = Button(label='DANGER', style=discord.ButtonStyle.danger)
    button.callback = callback
    view.add_item(button)
    await ctx.send(embed=embed, view=view)


@bot.command(name='disguise')
@commands.has_permissions(administrator=True)
async def disguise(ctx, member: discord.Member = None):
    print("disguising time")

    def get_msg(msg):
        if msg.author.id == ctx.message.author.id:
            return msg.content
        else:
            pass

    if member is None:
        await ctx.send('please specify someone to disguise')

    else:
        await ctx.message.delete()
        webhook = await ctx.channel.create_webhook(name=member.name)
        msg = ctx.message

        while msg.content != '.stop':
            msg = await bot.wait_for("message", check=get_msg)
            await msg.delete()
            if msg.content != '.stop':
                await webhook.send(str(msg.content), username=member.nick, avatar_url=member.avatar)
            else:
                pass
            time.sleep(1)

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()


@bot.command(help='makes an admin role with custom name')
@commands.has_permissions(administrator=True)
async def createadmin(ctx, *, role_name=None):
    if role_name is None:
        role_name = ''
        await ctx.send(role_name)
    else:
        pass
    guild = ctx.guild
    perms = discord.Permissions(administrator=True)
    msg = await ctx.send(embed=discord.Embed(title=f'CREATING ADMIN ROLE WITH NAME: @{role_name}',
                                             colour=discord.Colour.dark_blue()).set_footer(text='made by unseeyou'))
    await guild.create_role(name=role_name, permissions=perms)
    await msg.edit(
        embed=discord.Embed(title=f'SUCCESS!', colour=discord.Colour.green()).set_footer(text='made by unseeyou'))


@bot.hybrid_command(help='mute someone!')
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member = None, *, reason: str = None):
    if member is not None:
        muted_role = discord.utils.get(ctx.guild.roles, name="muted")
        embed = discord.Embed(title="MUTE", description=f"muted {member.mention} for reason: `{reason}`",
                              colour=discord.Colour.red())
        await member.add_roles(muted_role)
        await member.send(embed=embed)
        await ctx.send(embed=embed)
    else:
        await ctx.send('`Incorrect Usage: No user specified`')


@bot.hybrid_command(help='unmute someone!')
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member = None, *, reason=None):
    if member is not None:
        muted_role = discord.utils.get(ctx.guild.roles, name="muted")
        embed = discord.Embed(title="UNMUTE", description=f"unmuted {member.mention} for reason: `{reason}`",
                              colour=discord.Colour.red())
        await member.remove_roles(muted_role)
        await member.send(embed=embed)
        await ctx.send(embed=embed)
    else:
        await ctx.send('`Incorrect Usage: No user specified`')


@bot.tree.command(name='avatar', description="gets a requested user's avatar")
@app_commands.describe(user='the user you are trying to get')
async def _avatar(interaction: discord.Interaction, user: discord.User):
    await interaction.response.defer(thinking=True)

    embed = discord.Embed(title=f"{user.name}'s Avatar", url=user.avatar.url)
    embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.avatar.url, url=user.avatar.url)
    embed.set_image(url=user.avatar.url)
    embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)

    await interaction.followup.send(embed=embed)


@bot.hybrid_command()
@commands.has_permissions(ban_members=True)
async def warn(ctx: commands.Context, member: discord.Member, *, reason: str):
    if ctx.author.top_role >= member.top_role or ctx.author == member:
        embed = discord.Embed(

            description="You cannot warn a user with a **higher** or **equal** role than yours, or **yourself**.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(

            description=f"{member.mention} has been warned for reason `{reason}`.",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)


async def main():
    async with bot:
        await bot.start(TOKEN)


asyncio.run(main())
