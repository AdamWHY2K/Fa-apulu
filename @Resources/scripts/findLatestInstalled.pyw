from PyVDF import PyVDF
import vdf
from time import time
from shutil import copy
from sys import argv
from os import listdir

LocalVariables = []
completeDict = {}
idOrdered = []
MeterImage = 0
countLines = 0
persistantDict_content = []
foundPath = []
maniList = []
installedGames = []
countIDs = 0

def AddNonSteam(ID):
    #This must be called every time a non steam game is launched.
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
            #Import existing non steam game data

    for i in range(0, len(temp_persistantDict_content)):
        if ID in temp_persistantDict_content[i].split(":")[1][2:-3]:
            found = 1
            ErrorPosition = i
        else:
            pass
        #Record the position of the duplicate in the file if the app id is already recorded.

    if found == 1:
        for i in range(0, len(temp_persistantDict_content)):
            with open("..\\NonSteamDict.txt", "r") as persistantDict_file:
                lines = persistantDict_file.readlines()
                line_index = persistantDict_file.seek(i)

            SavedLines.insert(line_index, temp_persistantDict_content[i])
        del SavedLines[ErrorPosition]
        #Delete the duplicate line.
        SavedLines.append(str(tempDict) + "\n")
        #Add the updated timestamp to the rest of the recorded non steam game data
        copy("..\\NonSteamDict.txt", "..\\backup_NonSteamDict.txt")
        #Backup NonSteamDict incase file gets corrupted
        with open("..\\NonSteamDict.txt", "w") as persistantDict_file:
            for i in range(0, len(SavedLines)):
                persistantDict_file.write(SavedLines[i])
    else:
        with open("..\\NonSteamDict.txt", "a") as persistantDict_file:
            persistantDict_file.write(str(tempDict) + "\n") 

with open("..\\LocalVariables.txt", "r") as inFile:
	LocalVariables = inFile.readlines()
#Importing user defined path and steam account identifier.

try:
    readData = PyVDF()
    readData.load(LocalVariables[0][:-1] + "\\userdata\\" + LocalVariables[1] + "\\config\\localconfig.vdf")
    #LocalVariable[0] is user's steam path, LocalVariables[1] is user's steam account identifier.
    readData = readData.getData()
    #Using PyVDF to load localconfig.vdf into a dictionary, possible to extract everything using open() but this is much easier.
except UnicodeDecodeError:
        #readData = vdf.load(open(LocalVariables[0][:-1] + "\\userdata\\" + LocalVariables[1] + "\\config\\localconfig.vdf", errors="ignore"))
        print("uhoh")

readData = eval(repr(readData).lower())
#Many thanks to Cody Polera (https://github.com/cpolera) for recommending this KeyError fix.

readFolders = vdf.load(open(LocalVariables[0][:-1] + "\\steamapps\\libraryfolders.vdf", errors="ignore"))
readFolders = eval(repr(readFolders).lower())

foundPath.append(LocalVariables[0][:-1])
for i in readFolders["libraryfolders"]:
    if i.isdigit() == True:
        foundPath.append(readFolders["libraryfolders"][i]["path"])
        #Finding all user's install directories

for i in range(0, len(foundPath)):
    for ii in listdir(foundPath[i] + "\\steamapps"):
        if ii.endswith(".acf"):
            maniList.append(ii)
            installedGames.append(maniList[countIDs].split("_")[1].split(".")[0])
            countIDs += 1
            #Getting user's installed IDs

for i in installedGames:
    try:
        tempDict = {readData["userlocalconfigstore"]["software"]["valve"]["steam"]["apps"][i]["lastplayed"]:i}
        completeDict.update(tempDict)
        #Create a dictionary corresponding the unix timestamp from the last time the game was launched and the game's app id.
    except KeyError:
        pass
        #Steamworks Common Redistributables and probably other things have an appmanifest entry but no entry in localconfig.vdf so we skip them.

with open("..\\NonSteamDict.txt", "r") as persistantDict_file:
    for i in persistantDict_file:
        persistantDict_content.append(i)

for i in range(0, len(persistantDict_content)):
    tempDict = {persistantDict_content[i].split(":")[0][2:-1]:persistantDict_content[i].split(":")[1][2:-3]}
    completeDict.update(tempDict)
    #Add non steam id and unix timestamp to the completed dictionary, allowing them to be compared with steam games.

for i in sorted(completeDict, reverse = True):
    idOrdered.append(completeDict[i])
    #Sort app ids by latest played.

with open("..\\IncludeVariables.inc", "w") as temp:
    temp.write("[Variables]\n")

with open("..\\IncludeVariables.inc", "a") as out:
    for i in idOrdered:
        if countLines <= 34:
            countLines += 1
            MeterImage += 1
            out.write("MeterImageVar" + str(MeterImage) + " = " + i + "\n")
        else:
            break
        #Write the latest 35 app ids to a file to be read by rainmeter.

if __name__ == '__main__':
    try:
        globals()[argv[1]](argv[2])
    except IndexError:
        pass
#Allows AddNonSteam() to be called from cmd.
