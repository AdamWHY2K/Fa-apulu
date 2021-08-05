@echo off
:::
:::	___________________________________________________________________________________________________
:::	  /$$$$$$        /$$                         /$$      /$$ /$$   /$$ /$$     /$$ /$$$$$$  /$$   /$$
:::	 /$$__  $$      | $$                        | $$  /$ | $$| $$  | $$|  $$   /$$//$$__  $$| $$  /$$/
:::	| $$  \ $$  /$$$$$$$  /$$$$$$  /$$$$$$/$$$$ | $$ /$$$| $$| $$  | $$ \  $$ /$$/|__/  \ $$| $$ /$$/ 
:::	| $$$$$$$$ /$$__  $$ |____  $$| $$_  $$_  $$| $$/$$ $$ $$| $$$$$$$$  \  $$$$/   /$$$$$$/| $$$$$/  
:::	| $$__  $$| $$  | $$  /$$$$$$$| $$ \ $$ \ $$| $$$$_  $$$$| $$__  $$   \  $$/   /$$____/ | $$  $$  
:::	| $$  | $$| $$  | $$ /$$__  $$| $$ | $$ | $$| $$$/ \  $$$| $$  | $$    | $$   | $$      | $$\  $$ 
:::	| $$  | $$|  $$$$$$$|  $$$$$$$| $$ | $$ | $$| $$/   \  $$| $$  | $$    | $$   | $$$$$$$$| $$ \  $$
:::	|__/  |__/ \_______/ \_______/|__/ |__/ |__/|__/     \__/|__/  |__/    |__/   |________/|__/  \__/
:::
:::				Fa'apulu - A steam game launcher for rainmeter.
:::					Github: github.com/AdamWHY2K
:::
:::					I'd never say no to free pizza
:::				BTC: bc1qh8gx78jckh0dpzdzz8sd37y7mhq7s4vzj0xu6q
:::				BCH: bitcoincash:qzrqu0yecxka0p7sxr2g3fvpfcpg9x0awq3tf2m5ny
:::				ETH: 0x16560f37c1C908bb642f4e6D6Ac963Af044b9Dc7
:::	___________________________________________________________________________________________________

for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A

timeout 3

echo.
echo Installing python package, exit and install python if you don't have it installed.
pip install PyVDF
pip install vdf

echo.
echo Starting first phase: "getName"
start python @Resources\scripts\bat_getName.py
pause

echo.
echo Starting second and final phase: "copyHeaders" and "findLatest"
echo Please be patient, this could take a while.

start python @Resources\scripts\bat_findLatest.pyw
start python @Resources\scripts\bat_copyHeaders.pyw
pause
