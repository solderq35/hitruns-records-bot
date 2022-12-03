# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
from functions import *

EMBED_LIMIT = 20

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
#bot = commands.Bot(command_prefix='!')

@bot.command()
async def records(ctx, arg, amount:int=20):
    if arg == "all" or arg == "untied":
        if arg == 'all':
            if amount <= getNumberOfRuns('Ordered_Records.json'):
                length = (int)(str(amount))
            else:
                length = getNumberOfRuns('Ordered_Records.json')
            file = 'Ordered_Records.json'
        elif arg == 'untied':
            if amount <= getNumberOfRuns('Ordered_Untied_Records.json'):
                length = (int)(str(amount))
            else:
                length = getNumberOfRuns('Ordered_Untied_Records.json')
            file = 'Ordered_Untied_Records.json'
        
        rest = length % EMBED_LIMIT
        if rest != 0:
            pages = (length // EMBED_LIMIT) + 1
        else:
            pages = (length // EMBED_LIMIT)
            rest = EMBED_LIMIT
    
        for x in range(pages):
            embed=discord.Embed(title="Hitman 3 Records (Page " + str(x + 1) + ")", color=0xFF0000)
            if x < (pages - 1):
                pageSize = EMBED_LIMIT
            else:
                pageSize = rest
            for runs in range(pageSize):
            # wait ctx.send(type(runs + x * EMBED_LIMIT))
                data = getRecordData(file, (runs + x * EMBED_LIMIT))
                embed.add_field(name="Place " + str((runs + x * EMBED_LIMIT) + 1), value=data, inline=False)
            await ctx.send(embed=embed)
    else:
        await ctx.send('Bad Input!')
    
'''
@bot.command()
async def time(ctx, scoreString):
    try:
        score = int(scoreString)
    except ValueError:
        await ctx.send("Please, provide valid numbers")
        
    if score > 210000 or score < 8500:
        await ctx.send('input a proper score fucker')

    results = []
    for i in range(21):
        base = 5000 * i
        if i != 0:
            result = (210000 - ((score * 100000) / base)) * (3 / 400)

            if 3 <= result <= 300:
                results.append(format_time(result))

    msg = '\n'.join(results)

    await ctx.send(msg)
'''
    
@bot.command()
async def updateRecords(ctx):
    errorString = update()
    errorInt = int(0 if errorString is None else errorString)
    await ctx.send("Recorddata successfully updated with " + str(errorInt) + " errors")

bot.run(TOKEN)
