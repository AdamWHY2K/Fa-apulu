import logging
import vdf
import winreg
import os
import requests
import time
from wmi import WMI
from pymsgbox import confirm
from shutil import copy
import webbrowser
import sys
import glob


class Faapulu():
    def __init__(self) -> None:
        logging.basicConfig(
            filename="Fa'apulu_Status.log",
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y/%m/%d %I:%M:%S %p',
            filemode = 'w')
        logging.info("STARTING Fa'apulu")
        self.steam_registry_key = None
        self.steam_path = None
        self.steam_id = None
        self.user_data = None
        self.folders = None
        self.paths = []
        self.rainmeter_path = os.getcwd()
        self.header_files = []
        self.games_manifest = []
        self.installed_games = {}

    def read_registry(self):
        logging.info("Reading Steam registry key")
        self.steam_registry_key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, "Software\\Valve\\Steam", 0, winreg.KEY_READ)
        self.steam_path = winreg.QueryValueEx(self.steam_registry_key, "SteamPath")[0]
        winreg.CloseKey(self.steam_registry_key)
        self.steam_registry_key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, "Software\\Valve\\Steam\\ActiveProcess", 0, winreg.KEY_READ)
        self.steam_id = winreg.QueryValueEx(self.steam_registry_key, "ActiveUser")[0]
        winreg.CloseKey(self.steam_registry_key)
        if self.steam_id == 0:
            logging.error("\t\t\tSteam ID not found, ensure steam is running and you are logged in")
            logging.info("Retrying in 30 seconds")
            time.sleep(30)
            self.read_registry()

    def read_localconfig(self):
        logging.info(f"Reading localconfig.vdf @ {self.steam_path}/userdata/{self.steam_id}/config")
        self.user_data = eval(repr(vdf.load(open(f"{self.steam_path}/userdata/{self.steam_id}/config/localconfig.vdf", errors="ignore"))).lower())

    def read_libraryfolders(self):
        logging.info(f"Reading libraryfolders.vdf @ {self.steam_path}/steamapps")
        self.folders = eval(repr(vdf.load(open(f"{self.steam_path}/steamapps/libraryfolders.vdf", errors="ignore"))).lower())

    def set_user_paths(self):
        logging.info("Finding user's install paths")
        for i in self.folders["libraryfolders"]:
            if i.isdigit():
                self.paths.append(self.folders["libraryfolders"][i]["path"])
                logging.info(f'Found path: {self.folders["libraryfolders"][i]["path"]}')

    def find_headers(self):
        logging.info("Finding header images")
        os.chdir(f"{F.steam_path}/appcache/librarycache")
        self.header_files = glob.glob("*_header.jpg")

    def copy_headers(self):
        logging.info("Copying header images")
        for image in self.header_files:
            if image.replace("_header", "") in os.listdir(f"{self.rainmeter_path}\\@Resources\\headers"):
                pass
            else:
                copy(image, f'{self.rainmeter_path}\\@Resources\\headers\\{image.replace("_header", "")}')
        os.chdir(self.rainmeter_path)

    def set_games_manifest(self):
        for i in range(0, len(self.paths)):
            logging.info(fr"Finding manifest files @ {self.paths[i]}\steamapps")
            try:
                for file in os.listdir(fr"{self.paths[i]}\steamapps"):
                    if file.endswith(".acf"):
                        self.games_manifest.append(file.split("_")[1].split(".")[0])
            except FileNotFoundError:
                logging.warning(fr"Path invalid: {self.paths[i]}\steamapps")
                pass
                # User may have outdated paths in libraryfolders.vdf so we skip any currently invalid paths.
            except PermissionError:
                logging.warning(f"The device @ {self.paths[i]} is not ready")
                pass

    def set_installed_games(self):
        logging.info("Finding installed games")
        for i in self.games_manifest:
            try:
                self.installed_games.update([(i, self.user_data["userlocalconfigstore"]["software"]["valve"]["steam"]["apps"][i]["lastplayed"])])
                # Create a dictionary corresponding the game's app id and the unix timestamp from the last time the game was launched.
            except KeyError:
                logging.warning(f"App ID: {i} has a manifest entry, but no entry in localconfig.vdf")
                pass
                # Steamworks Common Redistributables and probably other things have an appmanifest entry but no entry in localconfig.vdf so we skip them.

    def write_app_id_variables(self):
        logging.info("Writing app_id_variables.inc")
        count = 0
        page_number = 0
        banner_number = 0
        Y = 0
        with open(f"{self.rainmeter_path}\\@Resources\\app_id_variables.inc", "w") as out:
            for game in sorted(self.installed_games, key=self.installed_games.get, reverse = True):
                if count < 35:
                    count += 1
                    out.write(f"""
[MeterImage{count}]
Meter=Image
X=0
Y={Y}
W=230
H=114
ImageName=#@#headers\{game}.jpg
LeftMouseUpAction=[steam://rungameid/{game}] [!CommandMeasure MeasureRun "Run"] [!Delay 5000][!Refresh "Fa'apulu"][!Delay 5000][!Refresh "Fa'apulu"]
MouseOverAction=[!SetOption MeterImageOverlay Y {Y}] [!SetOption MeterImageOverlay Hidden 0] [!Redraw]
MouseLeaveAction=[!SetOption MeterImageOverlay Hidden 1] [!Redraw]
Hidden=([MeasureImgNo]<>{page_number})
DynamicVariables=1\n""")
                    Y += 114
                    if banner_number >= 6:
                        banner_number = 0
                        Y = 0
                        page_number += 1
                    else:
                        banner_number += 1
                else:
                    logging.info("Finished writing app_id_variables.inc")
                    break
                #Write the latest 35 app ids to a file to be read by rainmeter.

class NonSteamGame():
    def __init__(self, ID = -1) -> None:
        self.id = ID
        self.persistant_content = []
        self.found = False
        self.error_position = 0
        self.line_index = 0
        self.saved_lines = []
        self.current_nonsteam_game = {int(time.time()):ID}
        self.nonsteam_path = f"{os.getcwd()}\\@Resources\\NonSteam.txt"

    def read_nonsteam(self):
        with open(self.nonsteam_path, "r") as persistant_file:
            for i in persistant_file:
                self.persistant_content.append(i)

    def find_duplicate(self):
        for i in range(0, len(self.persistant_content)):
            if self.id in self.persistant_content[i].split(":")[1][2:-2]:
                self.found = True
                self.error_position = i
            else:
                pass
            # Record the position of the duplicate in the file if the app id is already recorded.

    def write_nonsteam(self):
        if self.found: # If opened game already has entry in NonSteam.txt
            for i in range(0, len(self.persistant_content)):
                with open(self.nonsteam_path, "r") as persistant_file:
                    line_index = persistant_file.seek(i)
                self.saved_lines.insert(line_index, self.persistant_content[i])

            del self.saved_lines[self.error_position] # Delete the duplicate line.
            self.saved_lines.append(str(self.current_nonsteam_game)) # Add the updated timestamp to the rest of the recorded non steam game data
            copy(self.nonsteam_path, f"{self.nonsteam_path}.bak") # Backup NonSteam.txt incase file gets corrupted
            with open(self.nonsteam_path, "w") as persistant_file:
                for i in range(0, len(self.saved_lines)):
                    persistant_file.write(self.saved_lines[i])
        else:
            with open(self.nonsteam_path, "a") as persistant_file:
                persistant_file.write(str(self.current_nonsteam_game))

    def update_installed_games(self):
        for i in range(0, len(self.persistant_content)):
            F.installed_games.update({self.persistant_content[i].split(":")[1][2:-2]:self.persistant_content[i].split(":")[0][1:]})
            #Add non steam id and unix timestamp to the completed dictionary, allowing them to be compared with steam games.
    

def check_for_updates():
    current_version = "2.0.0"
    try:
        faapulu_github = requests.get("https://api.github.com/repos/AdamWHY2K/Fa-apulu/releases").json()
        latest_version = faapulu_github[0]["tag_name"][1:]
        changelog = faapulu_github[0]["body"]
        download_link = faapulu_github[0]["assets"][0]["browser_download_url"]
    except KeyError:
        latest_version = "0"
        changelog = "Unable to find changelog"
        download_link = "https://github.com/AdamWHY2K/Fa-apulu"
    
    if current_version < latest_version:
            if confirm(
            f"\tCurrent version: {current_version}\n\t Latest version: {latest_version}\n\n{changelog}\n\nDownload now?",
            "Fa'apulu - Update available",
            buttons=["OK", "Cancel"]) == "OK":
                webbrowser.open_new_tab(download_link) #Open download link in user's default browser
                logging.debug("Downloading update")
                raise SystemExit
            else:
                pass # Skip update this time, will ask again next time skin is refreshed or Rainmeter starts
    else:
        pass # User has latest version installed

def check_for_multiple_processes():
    count_processes = 0
    for i in WMI().Win32_Process(name="Fa-apulu.exe"):
        count_processes += 1
    if count_processes > 2:
        logging.debug("Exiting due to program already running.")
        raise SystemExit

if __name__ == "__main__":
    check_for_multiple_processes()
    check_for_updates()
    try:
        NS = NonSteamGame(sys.argv[1])
    except IndexError:
        NS = NonSteamGame()
    try:
        F = Faapulu()
        NS.read_nonsteam()
        if NS.id != -1: # If called with a non steam app id parameter
            NS.find_duplicate()
            NS.write_nonsteam()
        F.read_registry()
        F.read_localconfig()
        F.read_libraryfolders()
        F.set_user_paths()
        F.find_headers()
        F.copy_headers()
        F.set_games_manifest()
        F.set_installed_games()
        NS.update_installed_games()
        F.write_app_id_variables()
    except PermissionError: # Occasionally, seemingly arbitrarily, throws PermissionError.. I think maybe it can't write while Rainmeter is using the file
        pass # So just skip and hope that rainmeter is done reading the file by the next execution
