from discord.ext import commands
import discord


class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):  # if the slot is already taken by a player
            await interaction.response.send_message(
                'There is already a ' + ('X' if state == view.X else 'O') + ' in this slot!', ephemeral=True
            )
            return
        if view.current_player == view.X and view.players["X"] == interaction.user:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = f"It is now {view.players['O'].mention}'s turn (playing as O)"
        elif view.current_player == view.O and view.players["O"] == interaction.user:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = f"It is now {view.players['X'].mention}'s turn (playing as X)"
        else:
            await interaction.response.send_message(
                f'Someone else is playing as {"X" if view.current_player == view.O else "O"} already!', ephemeral=True
            )
            return

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f'{view.players["X"].mention} won as X!'
            elif winner == view.O:
                content = f'{view.players["O"].mention} won as O!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True
            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    X = -1
    O = 1
    Tie = 2

    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__()
        self.players: dict[str, discord.Member] = {"X": player1, "O": player2}
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class Coms(commands.Cog):
    @commands.hybrid_command(aliases=['noughtsandcrosses', 'XO'], help='a very scuffed tic tac toe game')
    async def tictactoe(self, ctx: commands.Context, opponent: discord.Member):
        embed = discord.Embed(description=f"{ctx.author.mention} (X) vs {opponent.mention} (O)",
                              colour=discord.Colour.og_blurple(),
                              title="Tic Tac Toe 1v1")
        await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe(player1=ctx.author, player2=opponent), embed=embed)


async def setup(bot):
    await bot.add_cog(Coms(bot))
