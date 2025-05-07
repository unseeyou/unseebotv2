import discord
import os
import flask
import asyncio
from discord.ext import commands, tasks

app = flask.Flask(__name__)


class Webserver(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.web_server.start()
        self.webserver_port = 8080

        @app.route("/")
        def index():
            return flask.render_template("index.html")

        @app.route("/stop")
        def stop_bot():
            asyncio.run_coroutine_threadsafe(self.bot.close(), loop=self.bot.loop)
            return flask.redirect("/")

        @app.route("/synctree")
        def status():
            print("syncing CommandTree")
            self.bot.loop.run_in_executor(None, self.bot.tree.sync)
            print("synced CommandTree")
            return flask.redirect("/")

    @tasks.loop()
    async def web_server(self):
        app.run(debug=True, host="0.0.0.0", port=self.webserver_port)
        print("SITE STARTED")

    @web_server.before_loop
    async def web_server_before_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Webserver(bot))
