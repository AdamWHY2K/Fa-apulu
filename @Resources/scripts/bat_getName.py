from os import listdir, path
from PyVDF import PyVDF
from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE

count = 0
curatedDir = []
readData = PyVDF()
completeDict = {}
foundAccount = None
openedKey = OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")

while True:
    answer = input("Is this your steam installation directory?\n" + QueryValueEx(openedKey, "InstallPath")[0] + "\nEnter \"Y\" or \"N\"\n\n")
    if answer.lower() == "y":
        steamPath = QueryValueEx(openedKey, "InstallPath")[0]
        break
    elif answer.lower() == "n":
        steamPath = input('Paste steam installation directory, e.g "C:\\Program Files\\Steam"\n\n')
        break
    else:
        print("Neither \"Y\" or \"N\" entered, try again.\n")

while True:
    if "Steam" not in steamPath or ":" not in steamPath or "\\" not in steamPath:
        print("Incorrect path detected, please try again\n\n")
        steamPath = input("Paste steam installation directory (The folder that steam.exe resides)\n\n")
    else:
        break
    #While loop keeps user from entering a tragically incorrect path
try:
    accountDir = listdir(steamPath + "\\userdata")
except FileNotFoundError:
    print("Critical error, check your steam directory. " + steamPath + "\\userdata doesn't exist?\n")
    input("Press enter then retry.\n")
    exit()
    #Try block catches exception if user enters the wrong steam path.

for i in accountDir:
    if accountDir[count] == "0":
        #print("skipping zero ", accountDir[count], "\nPlace in list: ", count)
        count += 1
        pass
    elif accountDir[count].isdigit():
        curatedDir.append(accountDir[count])
        #print("appending ", accountDir[count], "\nPlace in list: ", count)
        count += 1
    else:
        #print("skipping non digits ", accountDir[count], "\nPlace in list: ", count)
        count += 1
    #Steam has two folders in the user directory that don't belong to users, "0" and "ac" so we skip both of them.

count = 0
line = []

for i in curatedDir:
    #Iterating through all user folders in user directory.
    if path.isfile(steamPath + "\\userdata\\" + curatedDir[count] + "\\config\\localconfig.vdf"):
        try:
            readData.load(steamPath + "\\userdata\\" + curatedDir[count] + "\\config\\localconfig.vdf")
            readData = readData.getData()
            readData = eval(repr(readData).lower())
            #Many thanks to Cody Polera (https://github.com/cpolera) for recommending this KeyError fix.
            readData["userlocalconfigstore"]["friends"]["personaname"]
            completeDict.update({readData["userlocalconfigstore"]["friends"]["personaname"]:curatedDir[count]})
            #Adding user's steam name and steam account identifier to a dictionary.
            readData = PyVDF()
            count += 1
        except UnicodeDecodeError:
            #If user has a steam friend or steam group that has non standard characters PyVDF will throw a UnicodeDecodeError exception.
            #In this case we simply use open() with errors ignored, its uglier but functional.
            with open(steamPath + "\\userdata\\" + curatedDir[count] + "\\config\\localconfig.vdf", "r", errors='ignore') as altRead:
                line = altRead.readline(altRead.seek(altRead.read().find("\"PersonaName\"")))
                completeDict.update({line[16:-2]:curatedDir[count]})
                line = []
                count += 1

found = False

for i in completeDict:
    if found == False:
        answer = input("\nIs " + i + " the name of your steam account? Enter \"Y\" or \"N\"\n")
        if answer.lower() == "y":
            found = True
            foundAccount = completeDict[i]
            break

with open("@Resources\\LocalVariables.txt", "w") as outFile:
    outFile.write(steamPath + "\n" + foundAccount)
