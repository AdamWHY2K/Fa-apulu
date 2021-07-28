from os import chdir, listdir, getcwd
from subprocess import Popen
from glob import glob


LocalVariables = []
rainmeterPath = getcwd()

with open("..\\LocalVariables.txt", "r") as inFile:
	LocalVariables = inFile.readlines()

chdir(LocalVariables[0][:-1] + "\\appcache\\librarycache")
ToBeCopied = glob("*_header.jpg")
for i in ToBeCopied:
    if i.replace("_header", "") in listdir(rainmeterPath + "\\..\\headers"):
        pass
    else:
        Popen("copy " + i + " " + rainmeterPath + "\\..\\headers\\" + i.replace("_header", ""), shell = True)
