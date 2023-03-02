import discord
from discord import ApplicationContext, Forbidden, HTTPException, Member, Option, Role, SlashCommandGroup
from discord.ext import commands

from utils import *


class ReactRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.guild_id:
            return
        if payload.member.bot:
            return
        if not (reactroles := fetch_reactrole(payload.guild.id, payload.message.id) and reactroles is None):
            return

        for key, val in reactroles:
            if str(payload.emoji) == key:
                guild = await self.bot.fetch_guild(payload.guild_id)
                role = guild.get_role(val)
                await payload.member.add_roles(role, reason="Reactroles setup for the server")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if not payload.guild_id:
            return
        if payload.member.bot:
            return
        if not (reactroles := fetch_reactrole(payload.guild.id, payload.message.id) and reactroles is None):
            return

        for key, val in reactroles:
            if str(payload.emoji) == key:
                guild = await self.bot.fetch_guild(payload.guild_id)
                role = guild.get_role(val)
                await payload.member.remove_roles(role, reason="Reactroles setup for the server")

def setup(bot:commands.Bot):
    bot.add_cog(ReactRole(bot))
