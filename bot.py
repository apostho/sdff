import nextcord
import json
import urllib.request
import random
from nextcord.ext import commands
from simpledemotivators import Demotivator

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
            if message.attachments:
                f = open("src\genimages.txt", "a", encoding='utf-8')
                f.write(message.attachments[0].url + '\n')
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

@bot.command(aliases=['dem'])
async def demotivator(ctx):
    with open("src\genwords.txt", "r", encoding='utf-8') as f:
        genphrases = f.readlines()
    with open("src\genimages.txt", "r", encoding='utf-8') as f2:
        genimgs = f2.readlines()

    intparts = random.choice(range(1, 4))
    if intparts == 1:
        text1 = random.choice(genphrases).replace("\n", "")
    if intparts == 2:
        text1 = random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", "")
    if intparts == 3:
        text1 = random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", "")

    intparts2 = random.choice(range(1, 4))
    if intparts2 == 1:
        text2 = random.choice(genphrases).replace("\n", "")
    if intparts2 == 2:
        text2 = random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", "")
    if intparts2 == 3:
        text2 = random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", "")

    opener = urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    imgUrl = random.choice(genimgs)

    filename = 'src/attach.jpg'
    image_url = imgUrl
    urllib.request.urlretrieve(image_url, filename)


    
    demGen = Demotivator(text1, text2)
    demGen.create('src/attach.jpg')
    fileDem = nextcord.File("demresult.jpg", filename="demotivator.jpg")
    await ctx.send(file=fileDem)

bot.run(token)
