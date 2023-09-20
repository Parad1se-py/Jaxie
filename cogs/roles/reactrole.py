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

    rr_slash = SlashCommandGroup(name="reactrole", description="Reaction Role related commands.")

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
            
    @rr_slash.command(
        name="add",
        description="Add a new reactrole."
    )
    @commands.has_permissions(
        manage_roles=True
    )
    async def rr_add(self, ctx: ApplicationContext, msg_id: Option(str, required=True), emoji: Option(discord.Emoji, required=True), role: Option(discord.Role, required=True)):
        await ctx.defer()

        if role >= self.bot.top_role:
            return await hierarchy_error_embed(ctx, role=role)
        
        msg = await ctx.fetch_message(msg_id)
        await msg.add_reaction(emoji=emoji)
        add_reactrole(ctx.guild.id, msg_id, {emoji.id : role.id})

        await success_embed(
            ctx, f"added {role.name} as reactrole with emoji {emoji}"
        )

    @rr_slash.command(
        name="remove",
        description="Remove an existing reactrole."
    )
    @commands.has_permissions(
        manage_roles=True
    )
    async def rr_remove(self, ctx: ApplicationContext, msg_id: Option(str, required=True), emoji: Option(discord.Emoji, required=True)):
        await ctx.defer()

        msg = await ctx.fetch_message(msg_id)
        await msg.clear_reactions(emoji)

        if remove_reactrole(ctx.guild.id, msg_id, emoji.id):
            await success_embed(ctx, "removed reactrole")
        else:
            return await error_embed(ctx, "no reactrole found with that emoji.")
        
    @rr_slash.command(
        name="clear",
        description="Clear all reactroles from a single message."
    )
    @commands.has_permissions(
        manage_roles=True
    )
    async def rr_remove(self, ctx: ApplicationContext, msg_id: Option(str, required=True)):
        await ctx.defer()

        msg = await ctx.fetch_message(msg_id)
        await msg.clear_reactions()

        if remove_reactrole_set(ctx.guild.id, msg_id):
            await success_embed(ctx, "removed all reactroles")
        else:
            return await error_embed(ctx, "no reactroles found on that message.")
        
    @rr_slash.command(
        name="wipe",
        description="!! WIPES ALL REACTROLES FROM THE SERVER !!"
    )
    @commands.has_permissions(
        manage_roles=True
    )
    async def rr_remove(self, ctx: ApplicationContext):
        await ctx.defer()

        rr_data = fetch_reactrole(ctx.guild.id)

        if not rr_data:
            return await error_embed(ctx, "no reactroles found.")

        for key, val in rr_data:
            await ctx.fetch_message(key).clear_reactions()

        if wipe_reactroles(ctx.guild.id):
            await success_embed(ctx, "wiped all server reactroles")
        else:
            return await error_embed(ctx, "no reactroles found.")

def setup(bot:commands.Bot):
    bot.add_cog(ReactRole(bot))
