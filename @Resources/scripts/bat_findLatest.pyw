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

with open("@Resources\\LocalVariables.txt", "r") as inFile:
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

with open("@Resources\\NonSteamDict.txt", "r") as persistantDict_file:
    for i in persistantDict_file:
        persistantDict_content.append(i)

for i in range(0, len(persistantDict_content)):
    tempDict = {persistantDict_content[i].split(":")[0][2:-1]:persistantDict_content[i].split(":")[1][2:-3]}
    completeDict.update(tempDict)


for i in sorted(completeDict, reverse = True):
    idOrdered.append(completeDict[i])


with open("@Resources\\IncludeVariables.inc", "w") as temp:
    temp.write("[Variables]\n")

with open("@Resources\\IncludeVariables.inc", "a") as out:
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
