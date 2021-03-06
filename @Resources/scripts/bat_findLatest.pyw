from PyVDF import PyVDF
import vdf

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

readData = eval(repr(readData).lower())
#Many thanks to Cody Polera (https://github.com/cpolera) for recommending this KeyError fix.

for i in readData["userlocalconfigstore"]["software"]["valve"]["steam"]["apps"]:
    idList.append(i)
    #Extracting all ids into a list

for i in idList:
    try:
        tempDict = {readData["userlocalconfigstore"]["software"]["valve"]["steam"]["apps"][i]["lastplayed"]:i}
        completeDict.update(tempDict)
        #Create a dictionary corresponding the unix timestamp from the last time the game was launched and the game's app id.
    except KeyError:
        pass

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
