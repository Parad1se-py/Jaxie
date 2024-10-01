import contextlib
import discord
from discord.ext import commands

from utils import *


class GuildJoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 871422223913721876

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        invite = 'https://discord.com/api/oauth2/authorize?client_id=1040601339866124289&permissions=8798181256438&scope=bot%20applications.commands'
        support = 'https://discord.gg/VVfvtFV3qu'
        emd = discord.Embed(
            description=f'Hey! I\'m **Jaxie**.'
                        f'\n\nTo get started, use `/help`'
                        f'\n\n**Important Links**'
                        f'\n[Invite]({invite}) - Add me to another server!'
                        f'\n[Support Server]({support}) - Join my support server!',
            color=discord.Color.red(),
        )
        
        await create_server_collection(guild.id)

        def any_text_channel():
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    return channel

        intro = any_text_channel()

        if not intro:
            return
        with contextlib.suppress(discord.errors.Forbidden):
            await intro.send(embed=emd)
        logger = self.bot.get_channel(self.log_channel_id)  # type: ignore
        await logger.send(
            f'```fix\n- Joined [{guild.name}](ID:{guild.id})'
            f'\n- Owner ID: {guild.owner_id}'
            f'\n- Member Count: {guild.member_count}```'
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await clear_server_data(guild.id)
        logger = self.bot.get_channel(self.log_channel_id)
        await logger.send(
            f'```diff\n- Removed [{guild.name}](ID:{guild.id})'
            f'\n- Owner ID: {guild.owner_id}'
            f'\n- Member Count: {guild.member_count}```'
        )

def setup(bot:commands.Bot):
    bot.add_cog(GuildJoinLeave(bot))
