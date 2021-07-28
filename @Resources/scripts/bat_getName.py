from os import listdir, getcwd
from PyVDF import PyVDF

count = 0
curatedDir = []
readData = PyVDF()
completeDict = {}
foundAccount = None

print(getcwd())

path = input('Paste steam installation directory, e.g "C:\\Program Files\\Steam"\n\n')

accountDir = listdir(path + "\\userdata")

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

count = 0
line = []

for i in curatedDir:
    try:
        readData.load(path + "\\userdata\\" + curatedDir[count] + "\\config\\localconfig.vdf")
        readData = readData.getData()
        readData["UserLocalConfigStore"]["friends"]["PersonaName"]
        completeDict.update({readData["UserLocalConfigStore"]["friends"]["PersonaName"]:curatedDir[count]})
        readData = PyVDF()
        count += 1
    except UnicodeDecodeError:
        with open(path + "\\userdata\\" + curatedDir[count] + "\\config\\localconfig.vdf", "r", errors='ignore') as altRead:
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
    outFile.write(path + "\n" + foundAccount)
