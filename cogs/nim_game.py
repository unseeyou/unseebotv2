import discord
import random
from discord.ext import commands

class NimButton(discord.ui.Button):
    def __init__(self, num: int, total: int):
        super().__init__(style=discord.ButtonStyle.blurple, label=str(num), row=1)
        self.num = num
        self.gameover = False
        self.total = total
        self.turn = 'bot'
        self.current_value = total

    async def callback(self, interaction: discord.Interaction):
        try:
            assert self.view is not None
            self.current_value = self.view.get_value()
            self.current_value -= self.num
            view: NimGrid = self.view
            turn = view.get_turn()
            if turn == 'bot':
                embed = discord.Embed(title='It is not your turn!',
                                      description='press the bot turn button',
                                      colour=discord.Colour.dark_green())
                embed.set_footer(text='made by unseeyou')
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return 0
            total = self.total
            winner = view.check_board_winner()
            num = self.current_value
            content = f"**Marbles:** {num}"
            msg = f'You take away {self.num} marble{"." if self.num == 1 else "s."}'
            content += f"\n{msg}"
            view.update_turn('bot')
            self.turn = turn = view.get_turn()

            if total < 2:
                view.disable_all_buttons()
                self.gameover = True
            else:
                view.update_value(self.current_value)
                winner = view.check_board_winner()
                view.add_item(NimBotTurn())
            if winner:
                self.gameover = True
            if self.gameover:
                content = f"Game Over! You {'Win' if turn != 'human' else 'Lose'}!"
                view.disable_all_buttons()

            await interaction.response.edit_message(content=content, view=view)

        except Exception as err:
            print(err)


class NimStart(discord.ui.Button):
    def __init__(self, total):
        super().__init__(style=discord.ButtonStyle.green, label="PRESS ME TO START GAME", row=1)
        self.turn = 'human'
        self.total = total

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        self.style = discord.ButtonStyle.grey
        view: NimGrid = self.view
        num = view.get_value()
        msg = ''
        if num % 3 >= 1:
            view.update_turn('human')
            move = num % 3
            if num - move >= 0 and move != 0:
                num -= move
            else:
                move = random.randint(1, 2)
                num -= move
            msg = f'The bot takes away {move} marbles.'
        content = f"**Marbles:** {num}"
        content += f"\n{msg}"
        view.update_value(num)
        view.remove_item(self)

        await interaction.response.edit_message(content=content, view=view)


class NimHelpButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.red, label="How to Play", row=1)

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title='How to play nim', description='after getting a pile of marbles, the player and the bot take turns taking marbles away from the pile. You can only take either one or to marbles at a time. This game is literally not possible to win, if you do, send a screenshot to me (unseeyou).', colour=discord.Colour.dark_red())
        embed.set_footer(text='made by unseeyou')
        embed.set_author(icon_url=interaction.user.avatar.url, name=f'called by {interaction.user.name}')
        await interaction.response.send_message(embed=embed, ephemeral=True)


class NimBotTurn(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.grey, label="Click for Bot's Move", row=2)
        self.gameover = False
        self.turn = 'bot'
        self.current_value = 999  # lol

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        self.current_value = self.view.get_value()
        view: NimGrid = self.view
        num = self.current_value
        msg = ''
        if num % 3 >= 1:
            view.update_turn('human')
            move = num % 3
            if num - move >= 0 and move != 0:
                num -= move
                msg = f'The bot takes away {move} marble{"." if move == 1 else "s."}'
            else:
                move = random.randint(1, 2)
                num -= move
                msg = f'The bot takes away {move} marble{"." if move == 1 else "s."}'

            view.update_value(num)
            view.remove_item(self)

        content = f"**Marbles:** {num}"
        content += f"\n{msg}"
        winner = view.check_board_winner()
        if winner:
            self.gameover = True
        if self.gameover:
            turn = view.get_turn()
            content = f"Game Over! You {'Win' if turn != 'human' else 'Lose'}!"
            view.disable_all_buttons()

        await interaction.response.edit_message(content=content, view=view)


class EndInteraction(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.red, label="End Interaction", row=1)

    async def callback(self, interaction: discord.Interaction):
        view: NimGrid = self.view
        view.disable_all_buttons()
        await interaction.response.edit_message(view=view)


class NimGrid(discord.ui.View):
    def __init__(self, total):
        super().__init__()
        self.total = total
        self.turn = 'bot'
        self.board = [
            [0, 0]
        ]

        for x in range(2):
            for y in range(1):
                if x == 0:
                    self.add_item(NimButton(1, self.total))  # 1
                if x == 1:
                    self.add_item(NimButton(2, self.total))  # 2

        self.add_item(NimStart(total))
        self.add_item(NimHelpButton())
        self.add_item(EndInteraction())

    def disable_all_buttons(self):
        for child in self.children:
            child.disabled = True

    def enable_all_buttons(self):
        for child in self.children:
            child.disabled = False

    def update_value(self, value: int):
        self.total = value

    def check_board_winner(self):
        if self.total == 0:
            return True
        return False

    def update_turn(self, turn):
        self.turn = turn

    def get_turn(self):
        return self.turn

    def get_value(self):
        return self.total


class NimCommand(commands.Cog):
    @commands.hybrid_command(name='nim', description='launches the nim game')
    async def _nim(self, ctx, max_marbles: int):
        await ctx.defer()
        await ctx.send(f"__**GAME STARTED**__\n**Marbles:** {max_marbles if max_marbles > 1 else 'Not Enough!'}",view=NimGrid(total=max_marbles))


async def setup(bot):
    await bot.add_cog(NimCommand(bot))
