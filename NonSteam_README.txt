Please report any issues to https://github.com/AdamWHY2K/Fa-apulu/issues

Non steam games are supported:
Automatic method:
Run Spawn_NonSteamGame.py and follow its instructions.

Manual method:
1. Create .bat file to launch the non steam games .exe
2. Add this .bat file to steam as a non steam game
3. Create desktop shortcut for this non steam game, right click > properties, and copy the numbers. This shortcut can then be deleted.
4. Edit the same .bat file and add a line to run Fa-apulu.exe "Paste the numbers you copied here" 
 
This should look something like this:

chdir /d C:\Users\Adam\Documents\Rainmeter\Skins\Fa'apulu
.\@Resources\Fa-apulu.exe "15590464923526758400"
chdir /d C:\Riot Games\Riot Client
start "" RiotClientServices.exe
pause

5. Find a suitable banner image, I usually search for "GameName banner 460x215"
6. Save the image you find as "the string of numbers you copied.jpg", for example "11815543288612519936.jpg". Save this file in @Resources/headers