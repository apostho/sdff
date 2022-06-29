import discord
import json
import random
from discord.ext import commands

with open("config.json") as f:
    cdata = json.load(f)

token = cdata["token"]
prefix = cdata["prefix"]

ignorestr = [
    ',g',
    ',gen',
    ',generate',
    ',',
    'g',
    '.',
    ',,g',
    ',gg',
    '.g',
    '<@990349299873382430>'
]

endpoints = [
    '.',
    '!',
    '?',
    '...',
    '?!?!?!???!?!'
    '',
    '',
    '',
    '',
    '',
    '',
    ''
]

bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('booted up')


@bot.event
async def on_message(message):
    ctx = message.channel
    if any(item.lower() in message.content.lower() for item in ignorestr):
        pass
    else:
        if message.author == bot.user:
            return
        else:
            mescor = message.content
            mescorr = mescor.split()
            for item in mescorr:
                f = open("src\genwords.txt", "a", encoding='utf-8')
                f.write(item + '\n')
                f.close()
    if bot.user in message.mentions:
        with open("src\genwords.txt", "r", encoding='utf-8') as f:
            genphrases = f.readlines()

        intparts = random.choice(range(1, 4))
        endp = random.choice(endpoints)
        if intparts == 1:
            await ctx.send(random.choice(genphrases).replace("\n", "")+endp)
        if intparts == 2:
            await ctx.send(random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", "")+endp)
        if intparts == 3:
            await ctx.send(random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", "") +
                           endp)
    await bot.process_commands(message)


@bot.command(aliases=['g', 'gen'])
async def generate(ctx):
    with open("src\genwords.txt", "r", encoding='utf-8') as f:
        genphrases = f.readlines()
    intparts = random.choice(range(1, 4))
    if intparts == 1:
        await ctx.send(random.choice(genphrases).replace("\n", ""))
    if intparts == 2:
        await ctx.send(random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", ""))
    if intparts == 3:
        await ctx.send(random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", ""))

bot.run(token)
