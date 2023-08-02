import logging
import winreg
import os
import glob
import time
from shutil import copy
import vdf

log = logging.getLogger("Fa'apulu_log")

class Faapulu():
    def __init__(self, delay = 5000) -> None:
        log.info("STARTING Fa'apulu")
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
        self.ms_delay = delay

    def read_registry(self):
        log.info("Reading Steam registry key")
        try:
            self.steam_registry_key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, "Software\\Valve\\Steam", 0, winreg.KEY_READ)
            self.steam_path = winreg.QueryValueEx(self.steam_registry_key, "SteamPath")[0]
            winreg.CloseKey(self.steam_registry_key)
            self.steam_registry_key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, "Software\\Valve\\Steam\\ActiveProcess", 0, winreg.KEY_READ)
            self.steam_id = winreg.QueryValueEx(self.steam_registry_key, "ActiveUser")[0]
            winreg.CloseKey(self.steam_registry_key)
        except OSError as e:
            log.error(f"\t\t\t{e}")
        if self.steam_id == 0:
            log.error("\t\t\tSteam ID not found, ensure steam is running and you are logged in")
            log.info("Retrying in 30 seconds")
            time.sleep(30)
            self.read_registry()

    def read_localconfig(self):
        log.info(f"Reading localconfig.vdf @ {self.steam_path}/userdata/{self.steam_id}/config")
        self.user_data = eval(repr(vdf.load(open(f"{self.steam_path}/userdata/{self.steam_id}/config/localconfig.vdf", errors="ignore"))).lower())

    def read_libraryfolders(self):
        log.info(f"Reading libraryfolders.vdf @ {self.steam_path}/steamapps")
        self.folders = eval(repr(vdf.load(open(f"{self.steam_path}/steamapps/libraryfolders.vdf", errors="ignore"))).lower())

    def set_user_paths(self):
        log.info("Finding user's install paths")
        for i in self.folders["libraryfolders"]:
            if i.isdigit():
                self.paths.append(self.folders["libraryfolders"][i]["path"])
                log.info(f'Found path: {self.folders["libraryfolders"][i]["path"]}')

    def find_headers(self):
        log.info("Finding header images")
        try:
            os.chdir(f"{self.steam_path}/appcache/librarycache")
            self.header_files = glob.glob("*_header.jpg")
        except (FileNotFoundError, NotADirectoryError):
            log.error(f"\t\t\tDirectory: {self.steam_path}/appcache/librarycache not found")
        except PermissionError:
            log.error(f"\t\t\tFa-apulu doesn't have permission to access {self.steam_path}/appcache/librarycache")

    def copy_headers(self):
        try:
            for image in self.header_files:
                if image.replace("_header", "") in os.listdir(f"{self.rainmeter_path}\\@Resources\\headers"):
                    pass
                else:
                    log.info(f"Copying header image: {image}")
                    copy(image, f'{self.rainmeter_path}\\@Resources\\headers\\{image.replace("_header", "")}')
            os.chdir(self.rainmeter_path)
        except (FileNotFoundError, NotADirectoryError):
            log.error(f"\t\t\tDirectory: {self.rainmeter_path}\\@Resources\\headers not found")
        except PermissionError:
            log.error(f"\t\t\tFa-apulu doesn't have permission to access {self.rainmeter_path}\\@Resources\\headers")

    def set_games_manifest(self):
        for i, path in enumerate(self.paths):
            log.info(fr"Finding manifest files @ {path}\steamapps")
            try:
                for file in os.listdir(fr"{path}\steamapps"):
                    if file.endswith(".acf"):
                        self.games_manifest.append(file.split("_")[1].split(".")[0])
            except (FileNotFoundError, NotADirectoryError):
                log.warning(fr"Path invalid: {path}\steamapps")
                # User may have outdated paths in libraryfolders.vdf so we skip any currently invalid paths.
            except PermissionError:
                log.warning(f"The device @ {path} is not ready")

    def set_installed_games(self):
        log.info("Finding installed games")
        for ID in self.games_manifest:
            try:
                self.installed_games.update([(int(ID), int(self.user_data["userlocalconfigstore"]["software"]["valve"]["steam"]["apps"][ID]["lastplayed"]))])
                # Create a dictionary corresponding the game's app id and the unix timestamp from the last time the game was launched.
            except KeyError:
                log.warning(f"App ID: {ID} has a manifest entry, but no entry in localconfig.vdf")
                # Steamworks Common Redistributables and probably other things have an appmanifest entry but no entry in localconfig.vdf.

    def write_app_id_variables(self):
        log.info("Writing app_id_variables.inc")
        count = 0
        page_number = 0
        banner_number = 0
        y_axis = 0
        with open(f"{self.rainmeter_path}\\@Resources\\app_id_variables.inc", "w", encoding="UTF-8") as out:
            for game in sorted(self.installed_games, key=self.installed_games.get, reverse = True):
                if count < 35:
                    count += 1
                    out.write(fr"""
[MeterImage{count}]
Meter=Image
X=0
Y={y_axis}
W=230
H=114
ImageName=#@#headers\{game}.jpg
LeftMouseUpAction=[steam://rungameid/{game}] [!CommandMeasure MeasureRun "Run"] [!Delay {self.ms_delay}][!Refresh "Fa'apulu"][!Delay {self.ms_delay}][!Refresh "Fa'apulu"]
MouseOverAction=[!SetOption MeterImageOverlay Y {y_axis}] [!SetOption MeterImageOverlay Hidden 0] [!Redraw]
MouseLeaveAction=[!SetOption MeterImageOverlay Hidden 1] [!Redraw]
Hidden=([MeasureImgNo]<>{page_number})
DynamicVariables=1\n""")
                    y_axis += 114
                    if banner_number >= 6:
                        banner_number = 0
                        y_axis = 0
                        page_number += 1
                    else:
                        banner_number += 1
                else:
                    log.info("Finished writing app_id_variables.inc")
                    break
                #Write the latest 35 app ids to a file to be read by rainmeter.