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

gameName=input("Enter the name of the game's .exe:\n")

gamePath=input("Enter path to " + gameName + ".exe:\n")

skinPath=getcwd()


with open(gameName + ".bat", "w", encoding="utf-8") as temp:
    temp.write(f"""Move this file to {gamePath}
then add this file to steam as a non steam game (You may have to add the .exe, then change target in steam from .exe to .bat)
next right click on the new entry on steam and create a desktop shortcut
go to your desktop, right click the shortcut and go to properties
copy the long string of numbers, it should look similar to \"11653633573512463344\"
finally you can delete the desktop shortcut created by steam and return to the command line.""")

print(f"""
Move the newly created {gameName}.bat to {gamePath}
Add {gameName}.bat to steam as a non steam game
(You may have to add the .exe, then change target in steam from .exe to .bat)
Create desktop shortcut for this non steam game
Right click the shortcut and go to properties
Copy the numbers. This shortcut can then be deleted.
""")

input("Press enter once you've completed the above.")

appID = input("Enter the numbers you just copied:\n")

try:    
	with open(f"{gamePath}\\{gameName}.bat", "w", encoding="utf-8") as createLauncher:
		createLauncher.write(fr"""chdir /d "{skinPath}"
	.\@Resources\Fa-apulu.exe "{appID}"
	chdir /d "{gamePath}"
	start "" "{gameName}.exe"
	pause""")
except(FileNotFoundError, NotADirectoryError):
    print(f"Error: Couldn't find {gameName}.bat in {gamePath}")
    input("Press any key to quit")
    raise SystemExit
except PermissionError:
	print(f"This script doesn't have permission to access {gamePath}\\{gameName}.bat")
	input("Press any key to quit")
	raise SystemExit

print(f"Final step is to find a banner, save the image as {appID}.jpg in {skinPath}\\@Resources\\headers")
input("\nPress enter to find an image")

system(f"start \"\" \"https://www.google.com/search?&tbm=isch&q={gameName}+banner+460x215\"")

system(f'.\@Resources\Fa-apulu.exe "{appID}"') # Adding new game to NonSteam.json

input("\nFinished! Refresh Fa'apulu to see the new entry.")