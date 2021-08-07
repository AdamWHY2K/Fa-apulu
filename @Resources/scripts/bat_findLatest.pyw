from PyVDF import PyVDF
import vdf
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
#Importing user defined path and steam account identifier.

try:
    readData = PyVDF()
    readData.load(LocalVariables[0][:-1] + "\\userdata\\" + LocalVariables[1] + "\\config\\localconfig.vdf")
    #LocalVariable[0] is user's steam path, LocalVariables[1] is user's steam account identifier.
    readData = readData.getData()
    #Using PyVDF to load localconfig.vdf into a dictionary, possible to extract everything using open() but this is much easier.
except UnicodeDecodeError:
    readData = vdf.load(open(LocalVariables[0][:-1] + "\\userdata\\" + LocalVariables[1] + "\\config\\localconfig.vdf", errors="ignore"))

for i in readData["UserLocalConfigStore"]["Software"]["Valve"]["steam"]["Apps"]:
    idList.append(i)
    #Extracting all ids into a list

if "0" in idList:
    idList.pop()
    #For whatever reason steam sometimes has a 0 in the id list, but zero isn't actually an app id so we just remove it.

for i in idList:
    tempDict = {readData["UserLocalConfigStore"]["Software"]["Valve"]["steam"]["Apps"][i]["LastPlayed"]:i}
    completeDict.update(tempDict)
    #Create a dictionary corresponding the unix timestamp from the last time the game was launched and the game's app id.

with open("@Resources\\NonSteamDict.txt", "r") as persistantDict_file:
    for i in persistantDict_file:
        persistantDict_content.append(i)

for i in range(0, len(persistantDict_content)):
    tempDict = {persistantDict_content[i].split(":")[0][2:-1]:persistantDict_content[i].split(":")[1][2:-3]}
    completeDict.update(tempDict)
    #Add non steam id and unix timestamp to the completed dictionary, allowing them to be compared with steam games.

for i in sorted(completeDict, reverse = True):
    idOrdered.append(completeDict[i])
    #Sort app ids by latest played.

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
     #Write the latest 35 app ids to a file to be read by rainmeter.
