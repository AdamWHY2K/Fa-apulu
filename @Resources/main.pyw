import logging
import webbrowser
import sys
from pymsgbox import confirm
from wmi import WMI
import requests
import Faapulu
import NonSteam

log = logging.getLogger("Fa'apulu_log")
log.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y/%m/%d %I:%M:%S %p")
# Log to file
file_handler = logging.FileHandler("Fa'apulu_Status.log", "w")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)
# Log to stdout
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)


def check_for_updates():
    log.info("Checking for updates")
    current_version = "2.1.0"
    try:
        faapulu_github = requests.get("https://api.github.com/repos/AdamWHY2K/Fa-apulu/releases", timeout=30).json()
        latest_version = faapulu_github[0]["tag_name"][1:]
        changelog = faapulu_github[0]["body"]
        download_link = faapulu_github[0]["assets"][0]["browser_download_url"]
    except (requests.ConnectTimeout, KeyError):
        log.warning("Cannot connect to GitHub")
        latest_version = "0"
        changelog = "Unable to find changelog"
        download_link = "https://github.com/AdamWHY2K/Fa-apulu"
    if current_version < latest_version:
        if confirm(
        f"\tCurrent version: {current_version}\n\t Latest version: {latest_version}\n\n{changelog}\n\nDownload now?",
        "Fa'apulu - Update available",
        buttons=["OK", "Cancel"]) == "OK": # If user clicks OK
            webbrowser.open_new_tab(download_link) # Open download link in user's default browser
            log.info("Downloading update")
            raise SystemExit
        else:
            log.warning("Skipping update")
    else:
        log.info("Latest version installed")

def check_for_multiple_processes():
    for i, process in enumerate(WMI().Win32_Process(name="Fa-apulu.exe")):
        if i > 1:
            log.debug("Exiting due to program already running.")
            raise SystemExit

if __name__ == "__main__":
    try: # Don't check for multiple processes when adding a non-steam game as this might stop NonSteam.json from updating
        if sys.argv[1] != "-1":
            NS = NonSteam.Game(sys.argv[1])
        else:
            raise IndexError
    except IndexError:
        check_for_multiple_processes()
        NS = NonSteam.Game()
    check_for_updates()
    try:
        F = Faapulu.Faapulu(sys.argv[2])
    except IndexError:
        F = Faapulu.Faapulu()
    try:
        NS.read_nonsteam()
        if NS.id != -1: # If called with a non steam app id parameter
            NS.handle_duplicate()
            NS.write_nonsteam()
        F.read_registry()
        F.read_localconfig()
        F.read_libraryfolders()
        F.set_user_paths()
        F.find_headers()
        F.copy_headers()
        F.set_games_manifest()
        F.set_installed_games()
        NS.update_installed_games(F)
        F.write_app_id_variables()
    except PermissionError: # Occasionally, seemingly arbitrarily, throws PermissionError.. I think maybe it can't write while Rainmeter is using the file
        pass # So just skip and hope that rainmeter is done reading the file by the next execution