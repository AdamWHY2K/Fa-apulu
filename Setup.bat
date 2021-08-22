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
:::				BTC: bc1qfgj4tk2a7hzyxmmrgx4mvumef5f6yfey737xsj
:::				BCH: bitcoincash:qzrqu0yecxka0p7sxr2g3fvpfcpg9x0awq3tf2m5ny
:::				ETH: 0xB253acEedD0E98C7a38D81a0FDCEca7Cf2ED1dc7
:::				XMR: 47tW7pPZTW9LWxsB3KkWSgQgK9B5RH8yr9hPZ7jRofu8jTtPPxhpRVYjJvkK2EsYDsfpbMGBBQp5wNRrk4h6pPhG2rH1q8s
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
