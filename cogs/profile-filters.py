from PIL import Image
import os
import discord
from discord.ext import commands
from discord import app_commands


async def create_gif(member: discord.Member):
    base_width = 550
    bg = Image.new(mode="RGBA", size=(498, 670), color=(255, 255, 255, 255))

    triggered_bottom = Image.open("cogs/triggered.gif")
    width, height = triggered_bottom.size
    # print(width, height)

    filename = f"{member.id}-avatar.png"
    await member.avatar.save(filename)

    avatar = Image.open(filename)
    wpercent = (base_width / float(avatar.size[0]))
    hsize = int((float(avatar.size[1]) * float(wpercent)))
    avatar = avatar.resize((base_width, hsize), Image.Resampling.LANCZOS)

    bg.paste(avatar, (0, 0))
    bg.paste(triggered_bottom, (0, 498))
    frame_1 = bg.copy()
    triggered_bottom.seek(1)
    bg = Image.new(mode="RGBA", size=(498, 670), color=(255, 255, 255, 255))
    bg.paste(avatar, (-50, -40))
    bg.paste(triggered_bottom, (0, 498))
    frame_2 = bg.copy()
    triggered_bottom.seek(2)
    bg = Image.new(mode="RGBA", size=(498, 670), color=(255, 255, 255, 255))
    bg.paste(avatar, (-30, 0))
    bg.paste(triggered_bottom, (0, 498))
    frame_3 = bg

    frame_1.save(filename.replace(".png", ".gif"), save_all=True, append_images=[frame_2, frame_3], loop=0, duration=50)
    os.remove(filename)

    return filename.replace(".png", ".gif")


class ProfileFilters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def triggered(self, interaction: discord.Interaction, user: discord.Member = None):
        if user is None:
            user = interaction.user
        filename = await create_gif(user)
        await interaction.response.send_message(file=discord.File(filename))
        os.remove(filename)


async def setup(bot):
    await bot.add_cog(ProfileFilters(bot))
