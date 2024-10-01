import discord

from discord import ApplicationContext, Forbidden, HTTPException, Member, Option, Role, SlashCommandGroup, TextChannel
from discord.ext import commands

from utils import *


class Welcoming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded.")

    welcome_slash = SlashCommandGroup(name="welcome", description="Welcoming related commands.")

    @welcome_slash.command(
        name="set",
        description="Set the welcome message for your server."
    )
    async def welcome_set(self, ctx: ApplicationContext, channel: Option(TextChannel, required=True)):
        await ctx.defer()
        embed =discord.Embed(
            description="Use the [bot dashboard](https://www.website.com) to setup your server's welcoming system!"
        )
        await ctx.reply(embed=embed)
    
def setup(bot:commands.Bot):
    bot.add_cog(Welcoming(bot))
