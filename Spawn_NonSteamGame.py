from time import sleep
from os import getcwd, system


print("""
________________________________________________________________________________________________________________________
		  /$$$$$$        /$$                         /$$      /$$ /$$   /$$ /$$     /$$ /$$$$$$  /$$   /$$
		 /$$__  $$      | $$                        | $$  /$ | $$| $$  | $$|  $$   /$$//$$__  $$| $$  /$$/
		| $$  \ $$  /$$$$$$$  /$$$$$$  /$$$$$$/$$$$ | $$ /$$$| $$| $$  | $$ \  $$ /$$/|__/  \ $$| $$ /$$/ 
		| $$$$$$$$ /$$__  $$ |____  $$| $$_  $$_  $$| $$/$$ $$ $$| $$$$$$$$  \  $$$$/   /$$$$$$/| $$$$$/  
		| $$__  $$| $$  | $$  /$$$$$$$| $$ \ $$ \ $$| $$$$_  $$$$| $$__  $$   \  $$/   /$$____/ | $$  $$  
		| $$  | $$| $$  | $$ /$$__  $$| $$ | $$ | $$| $$$/ \  $$$| $$  | $$    | $$   | $$      | $$\  $$ 
		| $$  | $$|  $$$$$$$|  $$$$$$$| $$ | $$ | $$| $$/   \  $$| $$  | $$    | $$   | $$$$$$$$| $$ \  $$
		|__/  |__/ \_______/ \_______/|__/ |__/ |__/|__/     \__/|__/  |__/    |__/   |________/|__/  \__/
	
					Fa'apulu - A steam game launcher for rainmeter.
						Github: github.com/AdamWHY2K

				This script will create a .bat file used to launch non steam games. 
					      See README.txt for more information.
________________________________________________________________________________________________________________________""")

sleep(3)

gameName=input("Enter the name of the game's .exe:\n")

gamePath=input("Enter path to " + gameName + ".exe:\n")

skinPath=getcwd()


with open(gameName + ".bat", "w") as temp:
    temp.write("""Move this file to """ + gamePath + """
then add this file to steam as a non steam game
next right click on the new entry on steam and create a desktop shortcut
go to your desktop, right click the shortcut and go to properties
copy the long string of numbers, it should look similar to \"11653633573512463344\"
finally you can delete the desktop shortcut created by steam and return to the command line.""")

print("""
Move the newly created """ + gameName + """.bat to """ + gamePath + """
Add """ + gameName + """.bat to steam as a non steam game
Create desktop shortcut for this non steam game
Right click the shortcut go to properties
Copy the numbers. This shortcut can then be deleted.
""")

input("Press enter once you've completed the above.")

appID = input("Enter the numbers you just copied:\n")

with open(gamePath + "\\" + gameName + ".bat", "w") as createLauncher:
    createLauncher.write("""chdir /d """ + gamePath + """
start \"\" """ + gameName + """.exe
chdir /d """ + skinPath + """\\@Resources\\scripts
python findLatest.pyw AddNonSteam \"""" + appID + """\"
pause""")

print("Final step is to find a banner, save the image as " + appID + ".jpg in " + skinPath + "\\@Resources\\headers")
input("\nPress enter to find an image")

system("start \"\" \"https://www.google.com/search?&tbm=isch&q=" + gameName + "+banner+460x215\"")

sleep(5)

input("\nFinished! Next time you launch the game from steam it should also be updated next time you refresh Fa'apulu.")