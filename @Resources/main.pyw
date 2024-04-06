import logging
import sys
from wmi import WMI
import Faapulu
import NonSteam
import updater

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
    updater.check_for_updates("Fa'apulu", "https://api.github.com/repos/AdamWHY2K/Fa-apulu/releases", "2.1.1")
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