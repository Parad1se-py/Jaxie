import os

import discord
from dotenv import load_dotenv


load_dotenv()
bot = discord.Bot(intents=discord.Intents.all(), description="Jaxie is a mod-utility bot!", owner_id=718712985371148309)

@bot.slash_command()
async def load(ctx, name):
#	if ctx.author.id != 718712985371148309:
#		return
    bot.load_extension(f'cogs.{name}')
    await ctx.respond(f'Loaded {name}')

@bot.slash_command()
async def unloaded(ctx, name):
#	if ctx.author.id != 718712985371148309:
#		return
    bot.unload_extension(f'cogs.{name}')
    await ctx.respond(f'Unloaded {name}')

@bot.slash_command()
async def reload(ctx, name):
#	if ctx.author.id != 718712985371148309:
#		return
	bot.unload_extension(f'cogs.{name}')
	bot.load_extension(f'cogs.{name}')
	await ctx.respond(f'Reloaded {name}')

for foldername in os.listdir('./cogs'):
    for filename in os.listdir(f'cogs/{foldername}'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{foldername}.{filename[:-3]}')

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(f"Discord Version: {discord.__version__}")
	await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = f"/help | Watching over {len(bot.guilds)} servers!"))

bot.run('MTAzMzcxNDA0MjM2NTMwMDczNg.GA57h_.cTjrYvdVgL6tGT5f5v1O9gyZmdF_R5eslXa43Q')
