from ctypes import alignment
import os

# from tkinter import CENTER

import discord
from dotenv import load_dotenv
from discord.ext import commands
from functions import *
from table2ascii import table2ascii as t2a, Alignment

EMBED_LIMIT = 20

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# bot = commands.Bot(command_prefix='!')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
async def records(ctx, arg1, arg2="empty", arg3="empty"):
    # check if called for list of records
    if arg1 in ["all", "untied", "all-new", "untied-new"]:
        pages, rest, runData = await getPageData(arg1, arg2, EMBED_LIMIT)
        for x in range(pages):
            await ctx.send(
                embed=discordEmbed(pages, rest, runData, EMBED_LIMIT, x, "dict")
            )
    # check if called for list of specific board
    elif getBoardType(arg1) != False:
        boardType = getBoardType(arg1)
        if getBoardID(boardType, arg1) != False:
            if arg2.lower() == "saso":
                arg2 = "SA/SO"
            if getRatingID(boardType, arg2) != False:
                ratingID = getRatingID(boardType, arg2)
                boardData = getBoardData(
                    getBoardType(arg1), getBoardID(boardType, arg1), ratingID
                )
                if arg3 != "empty":
                    length = int(arg3)
                else:
                    length = len(boardData)
                pages, rest = getNumberOfPages(length, EMBED_LIMIT)
                for x in range(pages):
                    await ctx.send(
                        embed=discordEmbed(
                            pages, rest, boardData, EMBED_LIMIT, x, "list"
                        )
                    )
            else:
                await ctx.send("Invalid Rating Input. For more help, type `!docs`")
        else:
            await ctx.send(
                "No definitive match for name given. For more help, type `!docs`"
            )
    else:
        await ctx.send("Bad Input. For more help, type `!docs`")


"""
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
"""


# sum of bests
@bot.command()
async def sobs(ctx):
    SOBsDict = calcSobs()
    output = t2a(
        header=["Season(s)", "SA", "SA/SO", "Any%"],
        body=[
            ["Season 1", SOBsDict["SA S1"], SOBsDict["SA/SO S1"], SOBsDict["Any% S1"]],
            ["Season 2", SOBsDict["SA S2"], SOBsDict["SA/SO S2"], SOBsDict["Any% S2"]],
            ["Season 3", SOBsDict["SA S3"], SOBsDict["SA/SO S3"], SOBsDict["Any% S3"]],
            [
                "Trilogy",
                SOBsDict["SA Trilogy"],
                SOBsDict["SA/SO Trilogy"],
                SOBsDict["Any% Trilogy"],
            ],
        ],
        first_col_heading=True,
    )
    await ctx.send(f"```\n{output}\n```")


"""     for sobName, sobValue in SOBsDict.items():
        await ctx.send(sobName + ": " + str(sobValue)) """
# await ctx.send('Not available yet')


@bot.command()
async def docs(ctx):
    embed = discord.Embed(
        title="Command List / Help Doc",
        description="### [Click Here for Full Documentation if Needed](https://github.com/solderq35/hitruns-records-bot/blob/master/README.MD#commands) \n- !records all <amount>\n- !records all-new <amount>\n- !records untied <amount>\n- !records untied-new <amount>\n- !records <level name / fullgame category> <rating> <amount>\n- !sobs\n- !updateRecords\n- !updateRecords all <amount>\n- !updateRecords all-new <amount>\n- !updateRecords untied <amount>\n- !updateRecords untied-new <amount>\n- !updateRecords sobs\n\n- note: `<amount>` argument is optional. If not included, the maximum amount of records will be returned",
        color=0xFF5733,
    )
    await ctx.send(embed=embed)


@bot.command()
async def updateRecords(ctx, arg1="empty", arg2="empty"):
    ILBoardError, ILError, FGBoardError, FGError = update()
    if ILBoardError or ILError or FGBoardError or FGError:
        await updateRecords(ctx, arg1, arg2)
    else:
        await ctx.send("Recorddata successfully updated")
        if arg1 in ["all", "untied", "all-new", "untied-new"] and arg1 != "empty":
            pages, rest, runData = await getPageData(arg1, arg2, EMBED_LIMIT)
            for x in range(pages):
                await ctx.send(
                    embed=discordEmbed(pages, rest, runData, EMBED_LIMIT, x, "dict")
                )
        elif arg1 == "sobs" and arg1 != "empty":
            await sobs(ctx)
        elif arg1 == "empty":
            pass
        else:
            await ctx.send("Bad Input. For more help, type `!docs`")


bot.run(TOKEN)
