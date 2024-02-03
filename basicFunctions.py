import json
import datetime
import requests

dateFormat = "%Y-%m-%dT%H:%M:%SZ"
secondFormat = "PT%SS"
minuteFormat = "PT%MM%SS"
hourFormat = "PT%HH%MM%SS"
noSecondFormat = "PT%MM"
millisecondFormat = "PT%MM%S.%fS"
noMinutemillisecondFormat = "PT%S.%fS"


def getDictFromFile(jsonFile):
    file = open(jsonFile)
    dict = json.load(file)
    file.close()

    return dict


def getNumberOfRuns(jsonFile):
    runs = getDictFromFile(jsonFile)
    return len(runs)


def getNameOfBoard(jsonFile, ID):
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
                        try:
                            res = bool(datetime.datetime.strptime(time, hourFormat))
                            return hourFormat
                        except ValueError:
                            res = False


def orderDict(records_dict):
    unorderedRecords = getDictFromFile("data/" + records_dict)
    Dict_Ordered = {}

    for i in range(len(unorderedRecords.items())):
        dateNow = datetime.datetime.now()
        lowDate = dateNow + datetime.timedelta(hours=-1)
        for runs in unorderedRecords:
            currentDate = datetime.datetime.strptime(
                unorderedRecords[str(runs)].get("run", {}).get("submitted"), dateFormat
            )
            if currentDate <= lowDate:
                lowDate = currentDate
                lowDateKey = runs
        Dict_Ordered[i] = unorderedRecords[str(lowDateKey)]
        del unorderedRecords[str(lowDateKey)]

    with open("data/" + "Ordered_" + records_dict, "w") as write_file:
        json.dump(Dict_Ordered, write_file, indent=4)


def combineDicts(dict1, dict2, name):
    orderedDict1 = getDictFromFile(dict1)
    orderedDict2 = getDictFromFile(dict2)

    Combined_Dict = {}

    length1 = len(orderedDict1)
    length2 = len(orderedDict2)
    counter1 = 0
    counter2 = 0
    for i in range(length1 + length2):
        if counter1 < length1 and counter2 < length2:
            date1 = datetime.datetime.strptime(
                orderedDict1[str(counter1)].get("run", {}).get("submitted"), dateFormat
            )
            date2 = datetime.datetime.strptime(
                orderedDict2[str(counter2)].get("run", {}).get("submitted"), dateFormat
            )
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

    with open(name, "w") as write_file:
        json.dump(Combined_Dict, write_file, indent=4)


def requestBoards(boardType):
    boardDict = {}
    x = 0

    if boardType == "data/" + "campaign":
        x = 3
        boardRequest = requests.get(
            "https://www.speedrun.com/api/v1/games/j1ne5891/categories"
        )
    elif boardType == "data/" + "level":
        boardRequest = requests.get(
            "https://www.speedrun.com/api/v1/games/j1ne5891/levels"
        )

    boardObjects = boardRequest.json().get("data")
    try:
        for board in range(x, len(boardObjects)):
            boardDict[boardObjects[board].get("name")] = boardObjects[board].get("id")
    except TypeError:
        return True
    with open(boardType + "Dict.json", "w") as write_file:
        json.dump(boardDict, write_file, indent=4)
    return False


def untiedRecords(jsonFile):
    recordsDict = getDictFromFile("data/" + jsonFile)
    untiedRecordsDict = {}
    counter = 0

    for runs in recordsDict:
        if recordsDict[runs].get("isTied") == False:
            untiedRecordsDict[counter] = recordsDict[runs]
            counter = counter + 1

    with open("data/" + "Untied_" + jsonFile, "w") as write_file:
        json.dump(untiedRecordsDict, write_file, indent=4)


def inTimeFormat(rawSeconds):
    minutes = rawSeconds // 60
    seconds = rawSeconds % 60
    return str(minutes) + "m " + str(seconds) + "s"
