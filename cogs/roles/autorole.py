import discord
from discord import ApplicationContext, Forbidden, HTTPException, Interaction, Member, Option, Role, SlashCommandGroup
from discord.ext import commands

from utils import *


class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded.")

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        autoroles = fetch_autoroles(member.guild.id)
        if autoroles[0] == False:
            return

        try:
            for i in autoroles:
                role = member.guild.get_role(i)
                await member.add_roles(role, reason="Autoroles setup for the guild.")
        except Forbidden:
            # TODO: alert that unable to give roles due to lack of permissions
            print("no perms to give roles")
        except HTTPException:
            # TODO: alert that adding roles failed
            print("error on discord's side trying to add roles.")

    @commands.slash_command(
        name='autoroles',
        description='View the current autoroles of this server.',
        usage='/autoroles'
    )
    @commands.has_permissions(
        manage_roles=True
    )
    async def autoroles(self, ctx:ApplicationContext):
        await ctx.defer()
        autoroles = fetch_autoroles(ctx.guild.id)

        if autoroles[0] == False:
            return await ctx.respond(
                """You currently don't have any autoroles setup for this server!
                Use `/autorole add [role]` to add an autorole for this server."""
            )

        autoroles_str = "".join(f"<@&{i}>\n" for i in autoroles)
        
        return await ctx.respond(
            embed = discord.Embed(
                title=f"{ctx.guild.name}'s autoroles",
                description=autoroles_str
            )
        )

    ar = SlashCommandGroup('autorole', 'Slash group commands for autorole')

    @ar.command(
        name='add',
        description='Add an autorole that is given to users upon joining automatically.',
        usage='/autorole add [role]'
    )
    @commands.has_permissions(
        manage_roles=True
    )
    @commands.bot_has_permissions(
        manage_roles=True
    )
    async def ar_add(self, ctx: ApplicationContext, role: Option(Role, required=True)):
        await ctx.defer()

        if add_autorole(ctx.guild.id, role.id):
            await success_embed(
                ctx, f"added {role.name} as autorole"
            )
        
    @ar_add.error
    async def ar_add_error(interaction: Interaction, error):
        if isinstance(error, commands.BotMissingPermissions):
            await forbidden_error_embed(interaction, "manage_roles", "set autoroles")
        elif isinstance(error, commands.MissingPermissions):
            await missingperms_error_embed(interaction, "manage_roles", "set autoroles")
        else:
            raise error

    @ar.command(
        name='remove',
        description='Remove an autorole that is currently setup for the server.',
        usage='/autorole remove [role]'
    )
    @commands.has_permissions(
        manage_roles=True
    )
    async def ar_remove(self, ctx: ApplicationContext, role: Option(Role, required=True)):
        await ctx.defer()

        if not remove_autorole(ctx.guild.id, role.id):
            return await ctx.respond(
                """You don't have an autoroles setup for this server!
                You can add autoroles via `/autorole add [role]`.""")
        else:
            await success_embed(ctx, "removed autorole if it was set")

    @ar_remove.error
    async def ar_add_error(interaction: Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await missingperms_error_embed(interaction, "manage_roles", "remove autoroles")
        else:
            raise error


def setup(bot:commands.Bot):
    bot.add_cog(AutoRole(bot))
