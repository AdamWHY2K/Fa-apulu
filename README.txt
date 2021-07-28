Non steam games are supported:
1. Create .bat file to launch the non steam game's .exe
2. Add this .bat file to steam as a non steam game
3. Create desktop shortcut for this non steam game, right click, and copy the numbers. This shortcut can then be deleted.
4. Edit the same .bat file and add a line to run findLatest.pyw AddNonSteam "Paste the numbers you copied here" 
 
This should look something like this:

cd C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Riot Games
start "" VALORANT
cd C:\Users\Adam\Documents\Rainmeter\Skins\Fa'apulu\@Resources\scripts
python findLatest.pyw AddNonSteam "11815543288612519936"
pause

5. Find a suitable banner image, I usually search for "GameName banner 460x215"
6. Save the image you find as the string of numbers you copied.jpg, for example "11815543288612519936.jpg". Save this file in @Resources/headers