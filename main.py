from ctypes import alignment
import os
#from tkinter import CENTER

import discord
from dotenv import load_dotenv
from discord.ext import commands
from functions import *
from table2ascii import table2ascii as t2a, Alignment

EMBED_LIMIT = 20

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#bot = commands.Bot(command_prefix='!')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def records(ctx, arg, arg2='empty'):
    # check if called for list of records
    if arg == "all" or arg == "untied":
        length, file = setOutputLength(arg, arg2, EMBED_LIMIT)
        runData = getDictFromFile(file)
        pages, rest = getNumberOfPages(length, EMBED_LIMIT)
        for x in range(pages):
            await ctx.send(embed=discordEmbed(pages, rest, runData, EMBED_LIMIT, x, 'dict'))
    # check if called for list of specific board
    elif (getBoardType(arg) != False):
        boardType = getBoardType(arg)
        if (getBoardID(boardType, arg) != False):
            if (getRatingID(boardType, arg2) != False):
                ratingID = getRatingID(boardType, arg2)
                boardData = getBoardData(getBoardType(arg), getBoardID(boardType, arg), ratingID)
                length = len(boardData)
                pages, rest = getNumberOfPages(length, EMBED_LIMIT)
                for x in range(pages):
                    await ctx.send(embed=discordEmbed(pages, rest, boardData, EMBED_LIMIT, x, 'list'))
            else: await ctx.send('Invalid Rating Input')
        else:
            await ctx.send('No definitive match for name given')
    else:
        await ctx.send('Bad Input!')
    
'''
@bot.command()
async def time(ctx, scoreString):
    try:
        score = int(scoreString)
    except ValueError:
        await ctx.send("Please, provide valid numbers")
        
    if score > 209600 or score < 8500:
        await ctx.send('input a proper score fucker')

    results = []
    for i in range(21):
        base = 5000 * i
        if i != 0:
            result = (210000 - ((score * 100000) / base)) * 3 / 400

            if 3 <= result <= 300:
                results.append(format_time(result))

    msg = '\n'.join(results)

    await ctx.send(msg)
'''

# sum of bests
@bot.command()
async def sobs(ctx):
    SOBsDict = calcSobs()
    output = t2a(
        header=["Season(s)", "SA", "SA/SO", "Any%"],
        body=[["Season 1", SOBsDict["SA S1"], SOBsDict["SA/SO S1"], SOBsDict["Any% S1"]], \
        ["Season 2", SOBsDict["SA S2"], SOBsDict["SA/SO S2"], SOBsDict["Any% S2"]], \
        ["Season 3", SOBsDict["SA S3"], SOBsDict["SA/SO S3"], SOBsDict["Any% S3"]], \
        ["Trilogy", SOBsDict["SA Trilogy"], SOBsDict["SA/SO Trilogy"], SOBsDict["Any% Trilogy"]]],
        first_col_heading=True
    )
    await ctx.send(f"```\n{output}\n```")

"""     for sobName, sobValue in SOBsDict.items():
        await ctx.send(sobName + ": " + str(sobValue)) """
    # await ctx.send('Not available yet')
    
@bot.command()
async def updateRecords(ctx):
    ILError, FGError = update()
    if (ILError or FGError):
        await updateRecords(ctx)
    else:
        await ctx.send("Recorddata successfully updated")

bot.run(TOKEN)
