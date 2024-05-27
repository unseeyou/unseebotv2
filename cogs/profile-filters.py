from PIL import Image
import os
import discord
import traceback
from discord.ext import commands
from discord import app_commands


async def create_triggered_gif(member: discord.Member):
    base_width = 550
    bg = Image.new(mode="RGBA", size=(498, 670), color=(255, 255, 255, 255))
    red = Image.new(mode="RGBA", size=(498, 670), color=(215, 21, 0, 1))
    red.putalpha(85)

    triggered_bottom = Image.open("cogs/triggered.gif")

    filename = f"{member.id}-avatar.png"
    await member.avatar.save(filename)

    avatar = Image.open(filename)
    wpercent = (base_width / float(avatar.size[0]))
    hsize = int((float(avatar.size[1]) * float(wpercent)))
    avatar = avatar.resize((base_width, hsize), Image.Resampling.LANCZOS)

    bg.paste(avatar, (0, 0))
    bg.paste(triggered_bottom, (0, 498))
    bg.paste(red, (0, 0), red)
    frame_1 = bg.copy()
    triggered_bottom.seek(1)
    bg = Image.new(mode="RGBA", size=(498, 670), color=(255, 255, 255, 255))
    bg.paste(avatar, (-50, -40))
    bg.paste(triggered_bottom, (0, 498))
    bg.paste(red, (0, 0), red)
    frame_2 = bg.copy()
    triggered_bottom.seek(2)
    bg = Image.new(mode="RGBA", size=(498, 670), color=(255, 255, 255, 255))
    bg.paste(avatar, (-30, 0))
    bg.paste(triggered_bottom, (0, 498))
    bg.paste(red, (0, 0), red)
    frame_3 = bg

    frame_1.save(filename.replace(".png", ".gif"), save_all=True, append_images=[frame_2, frame_3], loop=0, duration=50)
    os.remove(filename)

    return filename.replace(".png", ".gif")


async def create_blushing_png(member: discord.Member):
    base_width = 1024
    bg = Image.new(mode="RGBA", size=(1024, 1024), color=(255, 255, 255, 255))
    pink = Image.new(mode="RGBA", size=(1024, 1024), color=(255, 128, 238, 255))
    pink.putalpha(100)
    filename = f"{member.id}-avatar.png"
    await member.avatar.save(filename)

    avatar = Image.open(filename)
    blush = Image.open("cogs/blush.png")

    wpercent = (base_width / float(avatar.size[0]))
    hsize = int((float(avatar.size[1]) * float(wpercent)))
    avatar = avatar.resize((base_width, hsize), Image.Resampling.LANCZOS)

    bg.paste(avatar, (0, 0))
    bg.paste(pink, (0, 0), pink)
    bg.paste(blush, (0, 0), blush)
    bg.save(filename)

    return filename


class ProfileFilters(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    avatar = app_commands.Group(name="avatar", description="commands for funny avatar filters and effects")

    @avatar.command(description="generates a Triggered GIF of the user's avatar")
    @app_commands.describe(user="the user whose avatar you want to use, leave blank to use yourself")
    async def triggered(self, interaction: discord.Interaction, user: discord.Member = None):
        await interaction.response.defer()
        try:
            if user is None:
                user = interaction.user
            filename = await create_triggered_gif(user)
            await interaction.followup.send(file=discord.File(fp=filename, filename="triggered.gif"))
            os.remove(filename)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)

    @avatar.command(name="blush", description="generates a blushing version of the user's avatar")
    @app_commands.describe(user="the user whose avatar you want to use, leave blank to use yourself")
    async def _blush(self, interaction: discord.Interaction, user: discord.Member = None):
        await interaction.response.defer()
        try:
            if user is None:
                user = interaction.user
            filename = await create_blushing_png(user)
            await interaction.followup.send(file=discord.File(fp=filename, filename="blushing.png"))
            os.remove(filename)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)


async def setup(bot):
    await bot.add_cog(ProfileFilters(bot))
