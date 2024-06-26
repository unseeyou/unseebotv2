import discord
import asyncio
from discord.ext import commands, tasks
from discord import app_commands

ffmpeg_options = {
    'options': '-vn',  # no video
}


async def play_music(voice):
    player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("portal_radio_loop.mp3"), volume=45)
    try:
        voice.play(player)
        return 0
    except Exception as err:
        print(err)
    return False


async def play_you_are_my_sunshine(voice):
    player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("you_are_my_sunshine.mp3"), volume=45)
    try:
        voice.play(player)
        return 0
    except Exception as err:
        print(err)
    return False


async def play_fly_me_to_the_moon(voice):
    player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("fly_me_to_the_moon_nge.mp3"), volume=45)
    try:
        voice.play(player)
        return 0
    except Exception as err:
        print(err)
    return False


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(help='joins your vc')
    async def join(self, ctx):
        """Joins a voice channel"""
        channel = ctx.author.voice.channel
        msg = await ctx.send('joining your vc')

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        else:
            await channel.connect()

        await msg.delete()

    @app_commands.command(description='play the radio')
    async def play(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        channel = interaction.user.voice.channel
        voice = await channel.connect(self_deaf=True)
        try:
            output = await play_music(voice)
        except Exception as err:
            output = str(err)

        if output == 0:
            await interaction.followup.send(f'Radio started by {interaction.user.name}')
            while voice is not None:
                if voice.is_playing():
                    await asyncio.sleep(0.2)
                if not voice.is_connected():
                    break
                if not voice.is_playing():
                    await play_music(voice)
        else:
            await interaction.followup.send(f'Error: {output}')

    @app_commands.command(description='my only sunshine')
    async def you_are_my_sunshine(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        channel = interaction.user.voice.channel
        voice = await channel.connect(self_deaf=True)
        try:
            output = await play_you_are_my_sunshine(voice)
        except Exception as err:
            output = str(err)

        if output == 0:
            await interaction.followup.send(f'{interaction.user.name} is singing a lullaby')
            while voice is not None:
                if voice.is_playing():
                    await asyncio.sleep(0.2)
                if not voice.is_connected():
                    break
                if not voice.is_playing():
                    await play_you_are_my_sunshine(voice)
        else:
            await interaction.followup.send(f'Error: {output}')

    @app_commands.command(description='and let me play among the stars')
    async def fly_me_to_the_moon(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        channel = interaction.user.voice.channel
        voice = await channel.connect(self_deaf=True)
        try:
            output = await play_fly_me_to_the_moon(voice)
        except Exception as err:
            output = str(err)

        if output == 0:
            await interaction.followup.send(f'{interaction.user.name} is having NGE PTSD')
            while voice is not None:
                if voice.is_playing():
                    await asyncio.sleep(0.2)
                if not voice.is_connected():
                    break
                if not voice.is_playing():
                    await play_fly_me_to_the_moon(voice)
        else:
            await interaction.followup.send(f'Error: {output}')

    @commands.hybrid_command(help='leaves the vc and stops playing audio')
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        msg = await ctx.send('stopping audio and leaving voice channel')
        await ctx.voice_client.disconnect()
        await msg.delete()


async def setup(bot):
    await bot.add_cog(Music(bot))
