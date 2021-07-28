from PyVDF import PyVDF
from time import time
from os import system
from shutil import copy
from sys import argv

LocalVariables = []
idList = []
completeDict = {}
idOrdered = []
MeterImage = 0
count = 0
persistantDict_content = []

with open("..\\LocalVariables.txt", "r") as inFile:
	LocalVariables = inFile.readlines()

readData = PyVDF()
readData.load(LocalVariables[0][:-1] + "\\userdata\\" + LocalVariables[1] + "\\config\\localconfig.vdf")
readData = readData.getData()

readData["UserLocalConfigStore"]["Software"]["Valve"]["steam"]["Apps"]

for i in readData["UserLocalConfigStore"]["Software"]["Valve"]["steam"]["Apps"]:
    idList.append(i)

idList.pop()

for i in idList:
    tempDict = {readData["UserLocalConfigStore"]["Software"]["Valve"]["steam"]["Apps"][i]["LastPlayed"]:i}
    completeDict.update(tempDict)

def AddNonSteam(ID):
    temp_persistantDict_content = []
    found = 0
    ErrorPosition = 0
    line_index = 0
    lines = None
    SavedLines = []
    tempDict = {str(int(time())):ID}
    with open("..\\NonSteamDict.txt", "r") as temp_persistantDict_file:
        for i in temp_persistantDict_file:
            temp_persistantDict_content.append(i)

    for i in range(0, len(temp_persistantDict_content)):
        if ID in temp_persistantDict_content[i].split(":")[1][2:-3]:
            found = 1
            ErrorPosition = i
        else:
            pass

    if found == 1:
        for i in range(0, len(temp_persistantDict_content)):
            with open("..\\NonSteamDict.txt", "r") as persistantDict_file:
                lines = persistantDict_file.readlines()
                line_index = persistantDict_file.seek(i)

            SavedLines.insert(line_index, temp_persistantDict_content[i])
        del SavedLines[ErrorPosition]
        with open("..\\NonSteamDict.txt", "w") as persistantDict_file:
            persistantDict_file.write(str(tempDict) + "\n")
    else:
        with open("..\\NonSteamDict.txt", "a") as persistantDict_file:
            persistantDict_file.write(str(tempDict) + "\n")

with open("..\\NonSteamDict.txt", "r") as persistantDict_file:
    for i in persistantDict_file:
        persistantDict_content.append(i)

for i in range(0, len(persistantDict_content)):
    tempDict = {persistantDict_content[i].split(":")[0][2:-1]:persistantDict_content[i].split(":")[1][2:-3]}
    completeDict.update(tempDict)


for i in sorted(completeDict, reverse = True):
    idOrdered.append(completeDict[i])


with open("..\\IncludeVariables.inc", "w") as temp:
    temp.write("[Variables]\n")

with open("..\\IncludeVariables.inc", "a") as out:
    for i in idOrdered:
        if count <= 34:
            count += 1
            MeterImage += 1
            out.write("MeterImageVar" + str(MeterImage) + " = " + i + "\n")
        else:
            break

if __name__ == '__main__':
    try:
        globals()[argv[1]](argv[2])
    except IndexError:
        pass
