from discord.ext import commands
from discord import app_commands

import asyncio


class Controls(commands.Cog):
    @commands.command(name='synctree', help='sync the command tree - unseeyou only')
    @commands.is_owner()
    async def sync_tree(self, ctx):
        msg = await ctx.send('Syncing command tree')
        async with ctx.typing():
            try:
                await app_commands.CommandTree.sync(guild=None)
                await msg.edit('Syncing commands tree | COMPLETE')
            except Exception as err:
                await msg.edit(f'Syncing commands tree | ERROR: [{err}]')
            await asyncio.sleep(240)


async def setup(bot):
    await bot.add_cog(Controls(bot))
