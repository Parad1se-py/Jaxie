import asyncio

import discord
from discord import ApplicationContext, TextChannel, Member, Option
from discord.ext import commands

from utils import *


class BasicMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # bot emotes
        self.success = '<:jaxie_done:1043740363803865089>'
        self.fail = '<:jaxie_mad:1043740361052393542>'

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded.")

    @commands.slash_command(
        name="kick",
        description="Kick a user mentioned if kickable.",
        usage="/kick [user] <reason>"
    )
    @commands.has_permissions(
        kick_members=True
    )
    async def kick(self, ctx: ApplicationContext, user: Option(Member, required=True), reason: Option(str, required=False)):
        await ctx.defer()

        try:
            await ctx.guild.kick(user, reason=reason)
        except discord.Forbidden:
            return await permission_error(ctx, "kick")
        except discord.HTTPException:
            return await http_error(ctx)

        return await success_embed(ctx, f"Kicked {user.name}", f"Reason: {reason}")

    @commands.slash_command(
        name="ban",
        description="Ban a user mentioned if bannable.",
        usage="/ban [user] <reason>"
    )
    @commands.has_permissions(
        ban_members=True
    )
    async def ban(self, ctx: ApplicationContext, user: Option(Member, required=True), reason: Option(str, required=False)):
        await ctx.defer()

        if user.top_role >= ctx.author.top_role or user.top_role >= self.bot.top_role:
            return await hierarchy_error(ctx, "ban")

        try:
            await ctx.guild.ban(user, reason=reason)
        except discord.Forbidden:
            return await permission_error(ctx, "ban")
        except discord.HTTPException:
            return await http_error(ctx)

        return await success_embed(ctx, f"Banned {user.name}", f"Reason: {reason}")

    @commands.slash_command(
        name="lock",
        description="Locks the specified channel for the [duration] if specified else forever.",
        usage="/lock [channel] <duration>"
    )
    @commands.has_permissions(
            manage_channels=True
    )
    async def lock(self, ctx: ApplicationContext, channel: Option(TextChannel, required=True), duration: Option(str, required=False)=None):
        await ctx.defer()

        if duration is None:
            duration = 'forever'

        try:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        except discord.Forbidden:
            return await permission_error(ctx, "lock")
        except discord.HTTPException:
            return await http_error(ctx)

        if duration != 'forever':
            await asyncio.sleep(duration)
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        return await success_embed(ctx, f"Locked {channel.mention}", f"Duration: {duration}")

    @commands.slash_command(
        name="unlock",
        description="Unlocks the specified channel if locked.",
        usage="/unlock [channel]"
    )
    @commands.has_permissions(
        manage_channels=True
    )
    async def unlock(self, ctx: ApplicationContext, channel: Option(TextChannel, required=True)):
        await ctx.defer()

        try:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        except discord.Forbidden:
            return await permission_error(ctx, "unlock")
        except discord.HTTPException:
            return await http_error(ctx)

        return await success_embed(ctx, f"Unlocked {channel.mention}")

    @commands.slash_command(
        name="purge",
        description="Purges the specified amount of messages.",
        usage="/purge [limit]"
    )
    @commands.has_permissions(
        manage_messages=True
    )
    async def purge(self, ctx: ApplicationContext, limit: Option(int, required=False)=5):
        await ctx.defer()

        try:
            await ctx.channel.purge(limit=limit+1)
        except discord.Forbidden:
            return await permission_error(ctx, "purge")
        except discord.HTTPException:
            return await http_error(ctx)

        return await success_embed(ctx, f"Purged {limit} messages from {ctx.channel.name}")


def setup(bot:commands.Bot):
    bot.add_cog(BasicMod(bot))
