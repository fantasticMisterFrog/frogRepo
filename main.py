import discord
from discord.ext import commands
import logging 
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
riddle = False
# ANIMALS_LST = ['-elephant', '-bee', '-fish', '-otter', '-cat', '-frog']
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
    # could be used to create a function that adds new facts
    with open('rock_facts.json', 'w') as f:
        json.dump(facts, f, indent=2)


# animals
def load_animals():
    with open('animals.json', 'r') as f:
        # l = [animal for animal in json.load(f)]
        # print(l)
        # for animal in l:
        #     animal = animal if animal.startswith('-') else '-' + animal # make sure all animals start with -
        return json.load(f)  


def save_animals(animals):
    with open('animals.json', 'w') as f:
        json.dump(animals, f, indent=2)


# riddles
def load_riddles():
    with open('riddles.json', 'r') as f:
        return json.load(f)


def save_riddles(riddles):
    with open('riddles.json', 'w') as f:
        json.dump(riddles, f, indent=2)
    
rock_facts = load_rock_facts() # list containing frog facts
animals = load_animals()  # list containing animal names
riddles = load_riddles()  # dictionary containing riddles
# print(riddles)

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
        await message.add_reaction('🐸')
    if message.content in {'-rock fact', '-frog fact'}:
        emoji = random.choice(('🤓', '🎓', '📖', '📚'))
        end_emoji = random.choice(('🤯', '🍄', '💥', '😮'))
        mmmm = 'm' * random.randint(1, 4)
        await message.channel.send(f'M{mmmm} have a rock fact {emoji}\n{random.choice(rock_facts)[:-1]} {end_emoji}')
    if message.content in animals:
        print("this ran")
        path = f'images/{message.content[1:]}'
        lst = os.listdir(path)
        await message.channel.send(file=discord.File(f'{path}/{random.choice(lst)}'))
    await bot.process_commands(message)  # always must be at the end of on_message to allow commands to be processed


@bot.command()
async def commands(ctx):
    animals_str = ' '.join(animals)
    help_text = (
        f"Available commands:\n"
        f"-rock/frog fact: Get a random frog fact\n"
        f"{animals_str}: Get animal's photo\n"
        f"-add_fact <fact>: Add a new frog fact\n"
        f"-remove_fact <fact>: Remove an existing frog fact\n"
        f"-add_animal_photo <animal>: Add a new animal photo\n"
        f"-remove_animal_photo <animal> <photo title>: Remove an animal photo\n"
        f"-add_animal <animal>: Add a new animal\n"
        f"-remove_animal <animal>: Remove an existing animal\n"
    )
    await ctx.send(help_text)


@bot.command()
async def virus(ctx):
    await ctx.send(MESSAGE)


# frog facts 🤓
@bot.command()
@commands.has_role(1395791649459798193)
async def add_fact(ctx, *, fact):
    print(fact)
    if fact == '': 
        await ctx.send('Toad fact 🤮')
        return
    if fact[-1] != '.':
        fact += '.'
    rock_facts.append(fact)
    save_rock_facts(rock_facts)
    await ctx.send('Fact added!')
    await ctx.send(f'New fact: {rock_facts[-1]}')
    await ctx.send(f'Current facts: {len(rock_facts)}')


@bot.command()
@commands.has_role(1395791649459798193)
async def remove_fact(ctx, *, fact):
    if fact == '':
        await ctx.send('Toad fact 🤮')
        return
    if fact[-1] != '.':
        fact += '.'
    if fact in rock_facts:
        rock_facts.remove(fact)
        save_rock_facts(rock_facts)
        await ctx.send('Fact removed!')
    else:
        await ctx.send('Fact not found!')
    await ctx.send(f'Current facts: {len(rock_facts)}')


#ANIMAL PICS!!!
@bot.command()
async def elephant(ctx):
    await ctx.send(file=discord.File(random.choice(os.listdir('images/elephant'))))

@bot.command()
async def bee(ctx):
    await ctx.send(file=discord.File(random.choice(os.listdir('images/bee'))))

@bot.command()
async def fish(ctx):
    await ctx.send(file=discord.File(random.choice(os.listdir('images/fish'))))

@bot.command()
async def otter(ctx):
    await ctx.send(file=discord.File(random.choice(os.listdir('images/otter'))))

@bot.command()
async def cat(ctx):
    await ctx.send(file=discord.File(random.choice(os.listdir('images/cat'))))

@bot.command()
async def frog(ctx):
    await ctx.send(file=discord.File(random.choice(os.listdir('images/frog'))))


# spaghetti
# Add/remove animal photos
@bot.command()
@commands.has_role(1395791649459798193)
async def add_animal_photo(ctx, *, animal):
    # attachment = ctx.message.attachments[0]
    if '-'+animal not in animals: # recall that members of animals are prefixed with '-'
        await ctx.send(f'Unknown animal: {animal}. Available animals: {"".join(animals)}')
        return False
    if len(ctx.message.attachments) == 0:
        await ctx.send('Attach photo to add!')
        return False
    for attachment in ctx.message.attachments:
        if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            await ctx.send('File must be an image')
            return False
        path = f'images/{animal}'
        ext = attachment.filename.split('.')[-1]
        filename = f'{path}/{len(os.listdir(path))+random.randint(1000, 9999999)}.{ext}'
        await attachment.save(filename)
    await ctx.send(f'Photo added for {animal}! Number of {animal} photos: {len(os.listdir(path))}')


@bot.command()
@commands.has_role(1395791649459798193)
async def remove_animal_photo(ctx, *, animal_photo):
    # basically -remove_animal_photo elephant <photo title>
    animal, photo = animal_photo.split(' ')
    folder = f'images/{animal}'
    if not os.path.exists(folder):
        await ctx.send(f'No photos found for {animal}.')
        return
    try: 
        os.remove(f'{folder}/{photo}')
        await ctx.send(f'Photo {photo} removed from {animal} photos. Number of photos: {len(os.listdir(folder))}')
    except FileNotFoundError:
        await ctx.send(f'Photo {photo} not found in {animal} photos.')


# Add/remove animals
@bot.command()
@commands.has_role(1395791649459798193)
async def add_animal(ctx, animal):
    if not animal.startswith('-'):
        animal = '-' + animal
    if animal in animals:
        await ctx.send(f'Animal {animal} already exists.')
        return
    animals.append(animal)
    os.makedirs(f'images/{animal[1:]}', exist_ok=True) 
    save_animals(animals)
    await ctx.send(f'Animal {animal} added! Current animals:\n{"\n".join(animals)}')


@bot.command()
@commands.has_role(1395791649459798193)
async def remove_animal(ctx, animal):
    if not animal.startswith('-'):
        animal = '-' + animal
    if animal not in animals:
        await ctx.send(f'Animal {animal} does not exist.')
        return
    animals.remove(animal)
    save_animals(animals)
    await ctx.send(f'Animal {animal[1:]} removed! Current animals:\n{"\n".join(animals)}')


# Riddles!!
@bot.command()
async def question(ctx):
    global riddle
    if not riddle:
        riddle = random.choice(list(riddles.keys()))
        print(riddle)
    await ctx.send(riddle)


@bot.command()
async def answer(ctx, *, answer):
    global riddle
    if not riddle:
        await ctx.send('No riddle is currently active. Use -riddle to start one.')
        return
    if answer.lower() == riddles[riddle].lower():
        await ctx.send(f'Correct! The answer was: {riddles[riddle]}')
        riddle = False
    else:
        await ctx.send(f'Incorrect!')


@bot.command()
async def give_up(ctx):
    global riddle
    if not riddle:
        await ctx.send('No riddle is currently active. Use -riddle to start one.')
        return
    await ctx.send(f'The answer was: {riddles[riddle]}')
    riddle = False


bot.run("", log_handler=handler, log_level=logging.DEBUG)
