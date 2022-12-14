import discord
from discord.ext import commands

import json
import datetime
import requests
import math
import re
from basicFunctions import *

GAME = 'j1ne5891'
VERSION_IL = 'ylpe1pv8=klrpdvwq'
VERSION_FG = '789d3g9n=814nxkjl'
DIFFICULTY_IL_PRO = 'r8r1dv7n=21dz5xpl'
# DIFFICULTY_IL_MASTER = 'p854xo3l=21g85z6l'
DIFFICULTY_FG_PRO = '5lypzk9l=4qyp9g6q'
# DIFFICULTY_FG_MASTER = ''

# translating ids to useable data for embed
#TODO: making it work for data from file and requests

def getRecordData(runs, counter, typeOfData):
    if typeOfData == 'dict':
        counter = str(counter)
    # getting rating and boardIDs from files
    levelID = runs[counter].get('run', {}).get('level')
    if levelID == None:
        levelID = runs[counter].get('run', {}).get('category')
        level = getNameOfBoard('campaignDict.json', levelID)
        ratingID = runs[counter].get('run', {}).get('values', {}).get('j84eq0wn')
        rating = getNameOfBoard('Ratings_FG.json', ratingID) 
        url_pattern = "/\bhttps?:\/\/\S+/gi"
        grun = runs[counter].get('run', {}).get('comment')
        grun2 = re.search("(?P<url>https?://[^\s]+)", grun).group("url")
        #print(grun2)
        if (grun2[-1]==")"):
            grun2 = grun2[:-1]
    else:
        level = getNameOfBoard('levelDict.json', levelID)
        ratingID = runs[counter].get('run', {}).get('category')
        rating = getNameOfBoard('Ratings_IL.json', ratingID)
        grun2 = " "
  
    # getting time in correct format
    timeObject = datetime.datetime.strptime(runs[counter].get('run', {}).get('times', {}).get('primary'), \
        getTimeFormat(runs[counter].get('run', {}).get('times', {}).get('primary')))
    if timeObject.hour == 1:
        time = timeObject.strftime("%Hh%Mm%Ss")
    elif (timeObject.hour == 0) and (timeObject.minute == 0):
        if timeObject.microsecond == 0:
            time = timeObject.strftime("%Ss")
        else:
            time = (timeObject.strftime("%S.%f")[:-3]) + "s"
    else:
        if timeObject.microsecond == 0:
            time = timeObject.strftime("%Mm%Ss")
        else:
            time = (timeObject.strftime("%Mm%S.%f")[:-3]) + "s"

    if runs[counter].get('run', {}).get('players')[0].get('rel') == 'user':
        playerID = runs[counter].get('run', {}).get('players')[0].get('id')
        player_request = requests.get('https://www.speedrun.com/api/v1/users/' + playerID)
        player = player_request.json().get('data', {}).get('names', {}).get('international')
    elif runs[counter].get('run', {}).get('players')[0].get('rel') == 'guest':
        player = runs[counter].get('run', {}).get('players')[0].get('name')
    
    date = runs[counter].get('run', {}).get('date')

    video = runs[counter].get('run', {}).get('videos').get('links')[0].get('uri')
    
    if (grun2 == " "):
        value = str(level) + " " + str(rating) + " in " + str(time) + " by " + str(player) + " on " + str(date) + "\nVideo: " + str(video)
    else:
        value = str(level) + " " + str(rating) + " in " + str(time) + " by " + str(player) + " on " + str(date) + "\nVideo: " + str(video) + "\n[Time Calc]({})".format(grun2)
    
    return value
        
def requestRecords(board):
    if board == 'IL':
        boardDict = getDictFromFile('levelDict.json')
        ratingsDict = getDictFromFile('Ratings_IL.json')
    elif board == 'FG':
        boardDict = getDictFromFile('campaignDict.json')
        ratingsDict = getDictFromFile('Ratings_FG.json')
    RecordsDict = {}

    for ratingName, ratingID in ratingsDict.items():
        for boardName, boardID in boardDict.items():
            if board == 'IL':
                leaderboard = \
                requests.get('https://www.speedrun.com/api/v1/leaderboards/' + GAME + '/level/' + boardID \
                + '/' + ratingID + '?var-' + VERSION_IL  + '&var-' + DIFFICULTY_IL_PRO)
            elif board == 'FG':
                leaderboard = \
                requests.get('https://www.speedrun.com/api/v1/leaderboards/' + GAME + '/category/' \
                + boardID + '?var-' + DIFFICULTY_FG_PRO + '&var-' + 'j84eq0wn=' + ratingID + \
                '&var-' + VERSION_FG)
            # check if runs are available and if they are tied
            runList = leaderboard.json().get('data', {}).get('runs')
            try:
                if len(runList) <= 1:
                    isTied = False
                elif runList[1].get("place") == 1:
                    isTied = True
                else:
                    isTied = False
                runList[0].update({"isTied": isTied})
                bestRun = runList[0]
                RecordsDict[(list(ratingsDict.keys()).index(ratingName) * len(boardDict)) \
                + (list(boardDict.keys()).index(boardName))] = bestRun
            except TypeError:
                return True
                
    with open(board + '_Records.json', 'w') as write_file:
        json.dump(RecordsDict, write_file, indent=4)
    return False

# Khunee timebot function
def format_time(time):
    if (time % 1 > .999):
        time = round(time)
    truncated = math.trunc(time * 1000) / 1000
    start = math.floor(time / 60)
    result = round(truncated - (start * 60), 3)
    if result < 10:
        result = "0" + str(result)
    return "{0}:{1}".format(start, result)

def getBoardType(input):
    levelDict = getDictFromFile('levelDict.json')
    campaignDict = getDictFromFile('campaignDict.json')
    for levelName, levelID in levelDict.items():
        if input.lower() in levelName.lower():
            return 'IL'
    for campaignName, campaignID in campaignDict.items():
        if input.lower() in campaignName.lower():
            return 'FG'
    return False

def getBoardID(boardType, input):
    levelDict = getDictFromFile('levelDict.json')
    campaignDict = getDictFromFile('campaignDict.json')
    i = 0
    boardID = ""
    if boardType == 'IL':
        for levelName, levelID in levelDict.items():
            if input.lower() in levelName.lower():
                i=i+1
                boardID = levelID
    elif boardType == 'FG':
        for campaignName, campaignID in campaignDict.items():
            if input.lower() in campaignName.lower():
                i=i+1
                boardID = campaignID
    if i == 1:
        return boardID
    return False

def getRatingID(boardType, input):
    ILRatingDict = getDictFromFile('Ratings_IL.json')
    FGRatingDict = getDictFromFile('Ratings_FG.json')
    if boardType == 'IL':
        for ratingName, ratingID in ILRatingDict.items():
            if input.lower() in ratingName.lower():
                return ratingID
    elif boardType == 'FG':
        for ratingName, ratingID in FGRatingDict.items():
            if input.lower() in ratingName.lower():
                return ratingID
    return False
    

def getBoardData(boardType, boardID, ratingID):
    if boardType == 'IL':
        return ILRequest(boardID, ratingID)
    elif boardType == 'FG':
        return FGRequest(boardID, ratingID)

# used for list of records in bot.py
def setOutputLength(tieStatus, lengthInput, embedLimit):
    if tieStatus == 'all':
        if lengthInput == 'empty':
            length = (int)(str(embedLimit))
        elif int(lengthInput) <= getNumberOfRuns('Ordered_Records.json'):
            length = (int)(str(lengthInput))
        else:
            length = getNumberOfRuns('Ordered_Records.json')
        file = 'Ordered_Records.json'
    elif tieStatus == 'untied':
        if lengthInput == 'empty':
            length = (int)(str(embedLimit))
        elif int(lengthInput) <= getNumberOfRuns('Ordered_Untied_Records.json'):
            length = (int)(str(lengthInput))
        else:
            length = getNumberOfRuns('Ordered_Untied_Records.json')
        file = 'Ordered_Untied_Records.json'
    return length, file

def getNumberOfPages(length, embedLimit):

    # arbitrarily reduce embed limit
    embedLimit = 10
    rest = length % embedLimit
    if rest != 0:
        pages = (length // embedLimit) + 1
    else:
        pages = (length // embedLimit)
        rest = embedLimit
    return pages, rest

def ILRequest(levelID, ratingID):
    leaderboard = \
    requests.get('https://www.speedrun.com/api/v1/leaderboards/' + GAME + '/level/' + levelID \
    + '/' + ratingID + '?var-' + VERSION_IL  + '&var-' + DIFFICULTY_IL_PRO)
    return leaderboard.json().get('data', {}).get('runs')

def FGRequest(campaignID, ratingID):
    leaderboard = \
    requests.get('https://www.speedrun.com/api/v1/leaderboards/' + GAME + '/category/' \
    + campaignID + '?var-' + DIFFICULTY_FG_PRO + '&var-' + 'j84eq0wn=' + ratingID + \
    '&var-' + VERSION_FG)
    return leaderboard.json().get('data', {}).get('runs')

def discordEmbed(pages, rest, runData, embedLimit, counter, typeOfData):
    embed=discord.Embed(title="Hitman 3 Records (Page " + str(counter + 1) + ")", color=0xFF0000)
    
    # arbitrarily reduce embed limit
    embedLimit = 10
    #print(embedLimit)
    #print(pages)
    if counter < (pages - 1):
        pageSize = embedLimit
    else:
        pageSize = rest
                
    for runs in range(pageSize):
        data = getRecordData(runData, (runs + counter * embedLimit), typeOfData)
        embed.add_field(name="Place " + str((runs + counter * (embedLimit)) + 1), \
        value=data, inline=False)
        
    fields = [embed.title, embed.description, embed.footer.text, embed.author.name]

    fields.extend([field.name for field in embed.fields])
    fields.extend([field.value for field in embed.fields])

    total = ""
    
    # testing total embed size
    """
    for item in fields:
        # If we str(discord.Embed.Empty) we get 'Embed.Empty', when
        # we just want an empty string...
        total += str(item) if str(item) != 'Embed.Empty' else ''

    #print(len(total))
    """
    
    return embed

def calcSobs():
    records = getDictFromFile("IL_Records.json")
    SOBs = {}
    sas3 = sas1 = sas2 = sasos3 = sasos1 = sasos2 = anys3 = anys1 = anys2 = 0
    offset = 36
    for runs in range(len(records.items())):
        if(runs > -1 and runs < 6):
            sas3 = sas3 + records[str(runs)].get('run', {}).get('times', {}).get('primary_t')
        elif(runs > 7 and runs < 14):
            sas1 = sas1 + records[str(runs)].get('run', {}).get('times', {}).get('primary_t')
        elif(runs > 13 and runs < 22):
            sas2 = sas2 + records[str(runs)].get('run', {}).get('times', {}).get('primary_t')
        elif(runs > -1 + offset and runs < 6 + offset):
            sasos3 = sasos3 + records[str(runs)].get('run', {}).get('times', {}).get('primary_t')
        elif(runs > 7 + offset and runs < 14 + offset):
            sasos1 = sasos1 + records[str(runs)].get('run', {}).get('times', {}).get('primary_t')
        elif(runs > 13 + offset and runs < 22 + offset):
            sasos2 = sasos2 + records[str(runs)].get('run', {}).get('times', {}).get('primary_t')
        elif(runs > -1 + offset*2 and runs < 6 + offset*2):
            anys3 = anys3 + records[str(runs)].get('run', {}).get('times', {}).get('primary_t')
        elif(runs > 7 + offset*2 and runs < 14 + offset*2):
            anys1 = anys1 + records[str(runs)].get('run', {}).get('times', {}).get('primary_t')
        elif(runs > 13 + offset*2 and runs < 22 + offset*2):
            anys2 = anys2 + records[str(runs)].get('run', {}).get('times', {}).get('primary_t')
    SOBs['SA S3'] = inTimeFormat(sas3)
    SOBs['SA S1'] = inTimeFormat(sas1)
    SOBs['SA S2'] = inTimeFormat(sas2)
    SOBs['SA/SO S3'] = inTimeFormat(sasos3)
    SOBs['SA/SO S1'] = inTimeFormat(sasos1)
    SOBs['SA/SO S2'] = inTimeFormat(sasos2)
    SOBs['Any% S3'] = inTimeFormat(anys3)
    SOBs['Any% S1'] = inTimeFormat(anys1)
    SOBs['Any% S2'] = inTimeFormat(anys2)
    SOBs['SA Trilogy'] = inTimeFormat(sas3 + sas1 + sas2)
    SOBs['SA/SO Trilogy'] = inTimeFormat(sasos3 + sasos1 + sasos2)
    SOBs['Any% Trilogy'] = inTimeFormat(anys3 + anys1 + anys2)
    with open('SOBs.json', 'w') as write_file:
        json.dump(SOBs, write_file, indent=4)
    return SOBs

def update():
    requestBoards('level')
    ILRequestResult = requestRecords('IL')
    orderDict('IL_Records.json')
    untiedRecords('Ordered_IL_Records.json')
    requestBoards('campaign')
    FGRequestResult = requestRecords('FG')
    orderDict('FG_Records.json')
    combineDicts('Untied_Ordered_IL_Records.json', 'Ordered_FG_Records.json', 'Ordered_Untied_Records.json')
    combineDicts('Ordered_IL_Records.json', 'Ordered_FG_Records.json', 'Ordered_Records.json')
    return ILRequestResult, FGRequestResult
