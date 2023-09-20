import discord
from discord import ApplicationContext, Forbidden, HTTPException, Member, Option, Role, SlashCommandGroup
from discord.ext import commands

from utils import *


class Welcoming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded.")
    
def setup(bot:commands.Bot):
    bot.add_cog(Welcoming(bot))
