import nextcord
import json
import urllib.request
import random
from discord.ext import commands
from nextcord.ext import commands
from simpledemotivators import Demotivator

intents = nextcord.Intents.default()
intents.message_content = True

with open("config.json") as f:
    cdata = json.load(f)
token = cdata["token"]
prefix = cdata["prefix"]
ignorestr = [
    #игнорируемые строки, которые не будет заносить в genwords.txt
    '@'
]
endpoints = [
    #знаки препинания в конце сообщения
    '.',
    '!',
    '?',
    `'...',
    '?!?!?!???!?!'
    '',
    '',
    '',
    '',
    '',
    '',
    ''
]
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')
@bot.event
async def on_ready():
    print('booted up')

@bot.event
async def on_message(message):
    ctx = message.channel
    #записывает слова в genwords.txt
    if any(item.lower() in message.content.lower() for item in ignorestr): #проверяет, есть ли в сообщении "банворд"
        pass
    else:
        if message.author == bot.user: #проверяет, является ли автор сообщения сам бот
            return
        else:
            mescor = message.content
            if len(mescor) < 75: #если в сообщении больше 75 символов - игнорирует, если меньше - заносит в genwords.txt
                mescorr = mescor.split()
                for item in mescorr:
                    #записывает слова в genwords.txt
                    f = open("src\genwords.txt", "a", encoding='utf-8')
                    f.write(item + '\n')
                    f.close()
                if message.attachments:
                    #записывает ссылку на вложение, если оно есть (для генерации изображений)
                    f = open("src\genimages.txt", "a", encoding='utf-8')
                    f.write(message.attachments[0].url + '\n')
                    f.close()
            else:
                pass
    if bot.user in message.mentions:
        #генерация сообщения, если бота пинганули
        with open("src\genwords.txt", "r", encoding='utf-8') as f:
            genphrases = f.readlines()
        #генерирует сообщение
        intparts = random.choice(range(1, 4))
        endp = random.choice(endpoints)
        if intparts == 1:
            await ctx.send(random.choice(genphrases).replace("\n", "")+endp)
        if intparts == 2:
            await ctx.send(random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", "")+endp)
        if intparts == 3:
            await ctx.send(random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", "") + " " + random.choice(genphrases).replace("\n", "") +
                           endp)
    await bot.process_commands(message) #продолжает обрабатывать команды

@bot.command(aliases = ['help']) #команда хелпа
async def info(ctx):
    await ctx.send('текст хелпа')
    
@bot.command(aliases=['g', 'gen']) #генерация сообщений командой
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

@bot.command(aliases=['d', 'dem'])
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
    await ctx.send('чзх', file=fileDem)

@bot.command(aliases=['dc', 'demcreate', 'demc'])
async def demotivatorcreate(ctx, text1:str=None, text2:str=None):
    with open("src\genimages.txt", "r", encoding='utf-8') as f2:
        genimgs = f2.readlines()
    if not text2:
        text2 = ' '
    if not text1:
        await ctx.send('ебланчик, ты забыл аргументы')
    else:
        if not ctx.message.attachments:
            await ctx.send('ебланчик ты картинку забыл')
        else:
            if len(text1) > 25:
                await ctx.send('один из аргументов слишком длинный, лаконичнее сука')
            elif len(text2) > 25:
                await ctx.send('один из аргументов слишком длинный, лаконичнее сука')
            else:
                opener = urllib.request.build_opener()
                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                urllib.request.install_opener(opener)
                imgUrl = ctx.message.attachments[0].url
                filename = 'src/attach.jpg'
                image_url = imgUrl
                urllib.request.urlretrieve(image_url, filename)
                fileDem = nextcord.File("demresult.jpg", filename="demotivator.jpg")
                demGen = Demotivator(text1, text2)
                demGen.create('src/attach.jpg')
                await ctx.send('чзх', file=fileDem)
    
bot.run(token)
