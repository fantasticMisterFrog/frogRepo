import discord
from discord.ext import commands
import logging # log the content of what's happening
from dotenv import load_dotenv
import random
import os
import json

load_dotenv() # loads environment variables from .env file
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default() # access permission
intents.message_content = True
intents.members = True 
bot = commands.Bot(command_prefix='-', intents=intents) 
ANIMALS_LST = ['-elephant', '-bee', '-fish', '-otter', '-cat']

MESSAGE = """Welcome to the new epidemic
If you fail to participate, you will bring shame onto discord and all frog kind. You have been infected. Now change your status to "DM me the word frog for a surprise."

The infection shall spread silently.

The only rule is to not spoil the game for others by telling people what saying frog does.

You have to keep the status for 2 months"""

# rock facts
def load_rock_facts():
    with open('rock_facts.json', 'r') as f:
        return json.load(f)


def save_rock_facts(facts):
    with open('rock_facts.json', 'w') as f:
        json.dump(facts, f, indent=2)


rock_facts = load_rock_facts() # list containing frog facts


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')

@bot.event
async def on_message(message):
    # reacts frog emoji when word frog is in message
    if message.author == bot.user:
        return
    if random.randint(0, 10) > 7 and ('frog' in message.content.lower() or 'phrog' in message.content.lower()):
        print(random.choice(rock_facts))
        await message.add_reaction('🐸')
    
    if message.content in {'-rock fact', '-frog fact'}:
        await message.channel.send('Mmm have a rock fact:\n ' + random.choice(rock_facts))

    await bot.process_commands(message)  # always must be at the end of on_message to allow commands to be processed

@bot.command()
async def virus(ctx):
    await ctx.send(MESSAGE)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)



# @client.event
# async def on_message(message):
#     if message.content in ANIMALS_LST:
#         print("this ran")
#         path = f'images/{message.content[1:]}'
#         lst = os.listdir(path)
#         await message.channel.send(file=discord.File(f'{path}/{random.choice(lst)}'))
# @client.command()
# async def elephant(ctx):
#     print('hi')
#     print(ctx.message.content)
    # print(ctx.message.Message)
    # await ctx.message.delete()
    # num = len(os.listdir('images/elephant'))
    # await ctx.send(file=discord.File(random.choice(os.listdir('images/elephant'))))

# @client.command()
# async def bee(ctx):
#     await ctx.send(file=discord.File(random.choice(os.listdir('images/bee'))))
#     # await ctx.send(file=discord.File(f'images/bee/{randint(0, 10)}.jpg'))

# @client.command()
# async def fish(ctx):
#     await ctx.send(file=discord.File(random.choice(os.listdir('images/fish'))))
# #     await ctx.send(file=discord.File(f'images/bee/{randint(0, 10)}.jpg'))

# @client.command()
# async def otter(ctx):
#     await ctx.send(file=discord.File(random.choice(os.listdir('images/otter'))))
#     # await ctx.send(file=discord.File(f'images/otter/{randint(0, 10)}.jpg'))
