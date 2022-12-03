import json
import datetime
import requests
import math

dateFormat = "%Y-%m-%dT%H:%M:%SZ"
secondFormat = "PT%SS"
minuteFormat ="PT%MM%SS"
noSecondFormat = "PT%MM"
millisecondFormat = "PT%MM%S.%fS"
noMinutemillisecondFormat = "PT%S.%fS"

GAME = 'j1ne5891'
VERSION_IL = 'ylpe1pv8=klrpdvwq'
VERSION_FG = '78962g08=p12dkr2q'
DIFFICULTY_IL_PRO = 'p854xo3l=gq7jpmpq'
# DIFFICULTY_IL_MASTER = 'p854xo3l=21g85z6l'
DIFFICULTY_FG_PRO = '5lypzk9l=4qyp9g6q'
# DIFFICULTY_FG_MASTER = ''

def getDictFromFile(jsonFile):
    file = open(jsonFile)
    dict = json.load(file)
    file.close()
    
    return dict

def orderDict(records_dict):
    file = open(records_dict)
    unorderedRecords = json.load(file)
    file.close()

    Dict_Ordered = {}

    for i in range (len(unorderedRecords.items())):
        dateNow = datetime.datetime.now()
        lowDate = dateNow + datetime.timedelta(hours=-1)
        for runs in unorderedRecords:
            currentDate = datetime.datetime.strptime(unorderedRecords[str(runs)].get('run', {}).get('submitted'), dateFormat)
            if (currentDate <= lowDate):
                lowDate = currentDate
                lowDateKey = runs
        Dict_Ordered[i] = unorderedRecords[str(lowDateKey)]
        del unorderedRecords[str(lowDateKey)]

    with open('Ordered_' + records_dict, 'w') as write_file:
        json.dump(Dict_Ordered, write_file, indent=4)


def combineDicts(dict1, dict2, name):
    file1 = open(dict1)
    orderedDict1 = json.load(file1)
    file1.close()

    file2 = open(dict2)
    orderedDict2 = json.load(file2)
    file2.close()

    Combined_Dict = {}
    
    length1 = len(orderedDict1)
    length2 = len(orderedDict2)
    counter1 = 0
    counter2 = 0
    for i in range(length1 + length2):
        if counter1 < length1 and counter2 < length2:
            date1 = datetime.datetime.strptime(orderedDict1[str(counter1)].get('run', {}).get('submitted'), dateFormat)
            date2 = datetime.datetime.strptime(orderedDict2[str(counter2)].get('run', {}).get('submitted'), dateFormat)
            if date1 <= date2:
                Combined_Dict[i] = orderedDict1[str(counter1)]
                counter1 = counter1 + 1
            elif date2 <= date1:
                Combined_Dict[i] = orderedDict2[str(counter2)]
                counter2 = counter2 + 1
        elif counter1 < length1:
            Combined_Dict[i] = orderedDict1[str(counter1)]
            counter1 = counter1 + 1
        elif counter2 < length2:
            Combined_Dict[i] = orderedDict2[str(counter2)]
            counter2 = counter2 + 1

    with open(name, 'w') as write_file:
        json.dump(Combined_Dict, write_file, indent=4)

def getNumberOfRuns(jsonFile):
    runs = getDictFromFile(jsonFile)
    return len(runs)

def getName(jsonFile, ID):
    runs = getDictFromFile(jsonFile)

    new_ke_lis = list(runs.keys())
    new_val = list(runs.values())
    new_pos = new_val.index(ID)
    return new_ke_lis[new_pos]

def getTimeFormat(time):
    res = True
    try:
        res = bool(datetime.datetime.strptime(time, millisecondFormat))
        return millisecondFormat
    except ValueError:
        try:
            res = bool(datetime.datetime.strptime(time, noMinutemillisecondFormat))
            return noMinutemillisecondFormat
        except ValueError:
            try:
                res = bool(datetime.datetime.strptime(time, secondFormat))
                return secondFormat
            except ValueError:
                try:
                    res = bool(datetime.datetime.strptime(time, minuteFormat))
                    return minuteFormat
                except ValueError:
                    try:
                        res = bool(datetime.datetime.strptime(time, noSecondFormat))
                        return noSecondFormat
                    except ValueError:
                        res = False

def getRecordData(jsonFile, counter):
    runs = getDictFromFile(jsonFile)

    levelID = runs[str(counter)].get('run', {}).get('level')
    if levelID == None:
        levelID = runs[str(counter)].get('run', {}).get('category')
        level = getName('campaignDict.json', levelID)
        ratingID = runs[str(counter)].get('run', {}).get('values', {}).get('j84eq0wn')
        rating = getName('Ratings_FG.json', ratingID) 
    else:
        level = getName('levelDict.json', levelID)
        ratingID = runs[str(counter)].get('run', {}).get('category')
        rating = getName('Ratings_IL.json', ratingID)
  
    timeObject = datetime.datetime.strptime(runs[str(counter)].get('run', {}).get('times', {}).get('primary'), getTimeFormat(runs[str(counter)].get('run', {}).get('times', {}).get('primary')))
    if timeObject.minute == 0:
        if timeObject.microsecond == 0:
            time = timeObject.strftime("%Ss")
        else:
            time = (timeObject.strftime("%S.%f")[:-3]) + "s"
    else:
        if timeObject.microsecond == 0:
            time = timeObject.strftime("%Mm%Ss")
        else:
            time = (timeObject.strftime("%Mm%S.%f")[:-3]) + "s"

    if runs[str(counter)].get('run', {}).get('players')[0].get('rel') == 'user':
        playerID = runs[str(counter)].get('run', {}).get('players')[0].get('id')
        player_request = requests.get('https://www.speedrun.com/api/v1/users/' + playerID)
        player = player_request.json().get('data', {}).get('names', {}).get('international')
    elif runs[str(counter)].get('run', {}).get('players')[0].get('rel') == 'guest':
        player = runs[str(counter)].get('run', {}).get('players')[0].get('name')
    
    date = runs[str(counter)].get('run', {}).get('date')

    value = str(level) + " " + str(rating) + " in " + str(time) + " by " + str(player) + " on " + str(date)
    
    return value

def requestBoards(boardType):
    boardDict = {}
    x = 0
    
    if boardType == 'campaign':
        x = 3
        boardRequest = requests.get('https://www.speedrun.com/api/v1/games/j1ne5891/categories')
    elif boardType == 'level':
        boardRequest = requests.get('https://www.speedrun.com/api/v1/games/j1ne5891/levels')

    boardObjects = boardRequest.json().get('data')
    for board in range(len(boardObjects) - x):
        boardDict[boardObjects[board + x].get('name')] = boardObjects[board + x].get('id')
    with open(boardType + 'Dict.json', 'w') as write_file:
        json.dump(boardDict, write_file, indent=4)
        
def requestRecords(board):
    if board == 'IL':
        boardDict = getDictFromFile('levelDict.json')
        ratingsDict = getDictFromFile('Ratings_IL.json')
    elif board == 'FG':
        boardDict = getDictFromFile('campaignDict.json')
        ratingsDict = getDictFromFile('Ratings_FG.json')
    RecordsDict = {}
    errors:int = 0

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
            
            runList = leaderboard.json().get('data', {}).get('runs')
            try:
                len(runList)
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
            except ValueError:
                errors = errors + 1
                
    with open(board + '_Records.json', 'w') as write_file:
        json.dump(RecordsDict, write_file, indent=4)
    return errors

def untiedRecords(jsonFile):
    recordsDict = getDictFromFile(jsonFile)
    untiedRecordsDict = {}
    counter = 0

    for runs in recordsDict:
        if(recordsDict[runs].get('isTied') == False):
            untiedRecordsDict[counter] = recordsDict[runs]
            counter = counter + 1

    with open('Untied_' + jsonFile, 'w') as write_file:
        json.dump(untiedRecordsDict, write_file, indent=4)

def format_time(time):
        rounded = round(time, 3)
        start = math.floor(time / 60)
        result = round(rounded - (start * 60), 3)
        if result < 10:
            result = "0" + str(result)
        return "{0}:{1}".format(start, result)
    
def update():
    requestBoards('level')
    requestRecords('IL')
    orderDict('IL_Records.json')
    untiedRecords('Ordered_IL_Records.json')
    requestBoards('campaign')
    requestRecords('FG')
    orderDict('FG_Records.json')
    combineDicts('Untied_Ordered_IL_Records.json', 'Ordered_FG_Records.json', 'Ordered_Untied_Records.json')
    combineDicts('Ordered_IL_Records.json', 'Ordered_FG_Records.json', 'Ordered_Records.json')
