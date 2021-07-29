from os import chdir, listdir, getcwd
from subprocess import Popen
from glob import glob


LocalVariables = []
rainmeterPath = getcwd()

with open("@Resources\\LocalVariables.txt", "r") as inFile:
	LocalVariables = inFile.readlines()
#Importing user defined path and steam account identifier.

chdir(LocalVariables[0][:-1] + "\\appcache\\librarycache")
#LocalVariable[0] is user's steam path
ToBeCopied = glob("*_header.jpg")
#Create list of files to be copied, using glob for wildcard functionality.
for i in ToBeCopied:
    if i.replace("_header", "") in listdir(rainmeterPath + "\\@Resources\\headers"):
        #If file already exists in rainmeter headers folder, skip.
        pass
    else:
        Popen("copy " + i + " " + rainmeterPath + "\\@Resources\\headers\\" + i.replace("_header", ""), shell = True)
