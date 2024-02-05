from ctypes import alignment
import os

# from tkinter import CENTER

import discord
from dotenv import load_dotenv
from discord.ext import commands
from functions import *
from table2ascii import table2ascii as t2a, Alignment
import time

EMBED_LIMIT = 20
LOG_LIMIT = 25

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# bot = commands.Bot(command_prefix='!')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
async def records(ctx, arg1, arg2="empty", arg3="empty"):
    # check if called for list of records
    if arg1 in ["all", "untied", "all-new", "untied-new"]:
        if await getPageData(arg1, arg2, EMBED_LIMIT) != False:
            pages, rest, runData = await getPageData(arg1, arg2, EMBED_LIMIT)
            for x in range(pages):
                await ctx.send(
                    embed=discordEmbed(pages, rest, runData, EMBED_LIMIT, x, "dict")
                )
        else:
            await ctx.send(
                "Bad Input, please provide a positive integer value for `<amount>` argument. For more help, type `!docs`"
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
                    try:
                        if int(arg3) <= len(boardData) and int(arg3) > 0:
                            length = int(arg3)
                            pages, rest = getNumberOfPages(length, EMBED_LIMIT)
                            for x in range(pages):
                                await ctx.send(
                                    embed=discordEmbed(
                                        pages, rest, boardData, EMBED_LIMIT, x, "list"
                                    )
                                )
                        else:
                            raise ValueError
                    except ValueError:
                        await ctx.send(
                            "Bad Input, please provide a positive integer value for `<amount>` argument. For more help, type `!docs`"
                        )
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
                await ctx.send(
                    "Invalid Rating Input. Rating input options: `sa`, `saso`, `any`. For more help, type `!docs`"
                )
        else:
            await ctx.send(
                'Bad Input.\n- If needed, reference `!levelNames` or `!fgNames` for a full list of level / fullgame category names.\n- Remember to surround level / fullgame category names with quotes, e.g `"season 3"`, or `"a gilded cage"`\n- For other help, type `!docs`'
            )
    else:
        await ctx.send(
            'Bad Input.\n- If needed, reference `!levelNames` or `!fgNames` for a full list of level / fullgame category names.\n- Remember to surround level / fullgame category names with quotes, e.g `"season 3"`, or `"a gilded cage"`\n- For other help, type `!docs`'
        )


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
        title="Command List Doc (Click Here for More)",
        url="https://github.com/solderq35/hitruns-records-bot/blob/master/README.MD#commands",
        description='- `!records all <amount>`\n  - Returns both tied and untied records, sorted by oldest to newest\n- `!records all-new <amount>`\n  - Returns both tied and untied records, sorted by newest to oldest\n- `!records untied <amount>`\n  - Returns untied records, sorted by oldest to newest\n- `!records untied-new <amount>`\n  - Returns untied records, sorted by newest to oldest\n- `!records <level name / fullgame category> <rating> <amount>`\n  - Returns a single leaderboard for a level / fullgame category and rating\n  - Use `!levelNames` or `!fgNames` for a full list of level names / fullgame category names respectively\n  - Any substring of a `<level name>` or `<fullgame category>` long enough to uniquely identify it will work, e.g. either `showstopper` or `paris` would be valid\n  - Any level or fullgame category name you input that contains a space (e.g. `"season 3"` or `"a gilded cage"`) should be surrounded by quotes\n  - Valid `<rating>` inputs: `sa`, `saso`, or `any`\n  - Unlike the other commands listed here, even if Recorddata has not been updated recently, this command will still return up-to-date results\n- `!sobs`\n  - Calculates theoretical best times for full game categories, by summing up individual level record times\n- `!getLogs`\n  - See when Recorddata was last updated. Tracks both manual updates and cron job automated updates (daily at 12 PM UTC, or <t:1675425600:t> local time)\n- `!updateRecords`\n  - Update Recorddata manually if you need more precision than last 24 hours\n  - Can also be "queued" with some other commands, e.g. `!updateRecords all-new <amount>`, `!updateRecords untied`, or `!updateRecords sobs`\n\n**Troubleshooting**:\n- Bot will be down for a minute or two at <t:1675425600:t> each day for data update\n- `<amount>` is optional. If not set, the max amount of records will be returned\n- Commands (anything starting with `!`) are case-sensitive, but arguments are not case-sensitive\n- Arguments should be provided in the same order as they are listed above',
        color=0xFF5733,
    )
    await ctx.send(embed=embed)


@bot.command()
async def levelNames(ctx):
    levelNames = getLevelNames()
    embed = discord.Embed(
        title="Level Names",
        description=("\n- " + "\n- ".join(levelNames)),
        color=0xFF5733,
    )
    await ctx.send(embed=embed)


@bot.command()
async def fgNames(ctx):
    fgNames = getFullGameNames()
    embed = discord.Embed(
        title="Full Game Categories",
        description=("\n- " + "\n- ".join(fgNames)),
        color=0xFF5733,
    )
    await ctx.send(embed=embed)


@bot.command()
async def getLogs(ctx):
    if os.path.isfile("update.log"):
        with open("update.log", "r") as file:
            logs = file.read()
        logOuputArr = []
        for line in logs.split("\n"):
            if len(line.split(" | ")) > 1:
                # discord timestamp format to render in user's local timezone: https://discord.com/developers/docs/reference#message-formatting
                logOuputArr.append(
                    "- <t:"
                    + line.split(" | ")[0]
                    + ":f>"
                    + " | `"
                    + line.split(" | ")[1]
                    + "`"
                )
        embed = discord.Embed(
            title="Recorddata Update Logs (Up to " + str(LOG_LIMIT) + " Most Recent)",
            description=("\n".join(logOuputArr))
            + "\n\nIf it's been a while since the last update, consider running `!updateRecords` again.",
            color=0xFF5733,
        )
        await ctx.send(embed=embed)
        file.close()
    else:
        await ctx.send("No logs found")


@bot.command()
async def updateRecords(ctx, arg1="empty", arg2="empty"):
    ILBoardError, ILError, FGBoardError, FGError = await update()
    if ILBoardError or ILError or FGBoardError or FGError:
        print("Error updating records, trying again")
        await updateRecords(ctx, arg1, arg2)
    else:
        print("Recorddata successfully updated")
        await ctx.send("Recorddata successfully updated")
        await updateLog(
            "update.log", str(int(time.time())) + " | manual update" + "\n", LOG_LIMIT
        )
        if arg1 in ["all", "untied", "all-new", "untied-new"] and arg1 != "empty":
            if await getPageData(arg1, arg2, EMBED_LIMIT) == False:
                await ctx.send(
                    "Bad Input, please provide a positive integer value for `<amount>` argument. For more help, type `!docs`"
                )
            else:
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
