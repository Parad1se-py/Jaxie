from utils import *

import discord
from discord import ApplicationContext
from discord.ext import commands


class ErrorHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded.")

	@commands.Cog.listener()
	async def on_command_error(self, ctx:ApplicationContext, error):
		if isinstance(error, commands.MissingPermissions):
			permission_error(ctx, "execute the command.")

def setup(bot:commands.Bot):
	bot.add_cog(ErrorHandler(bot))
