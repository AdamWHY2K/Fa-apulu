import os
import json
from shutil import copy
import logging
import time

log = logging.getLogger("Fa'apulu_log")

class Game():
    def __init__(self, ID = -1) -> None:
        log.info("STARTING NonSteam")
        self.id = ID
        self.persistant_content = {}
        self.current_nonsteam_game = {ID:int(time.time())}
        self.nonsteam_path = f"{os.getcwd()}\\@Resources\\NonSteam.json"

    def read_nonsteam(self):
        try:
            with open(self.nonsteam_path, "r", encoding="UTF-8") as json_file:
                self.persistant_content = json.load(json_file)
                log.info("Non steam games imported")
        except json.JSONDecodeError:
            log.info("No non-steam games detected")
            
    def handle_duplicate(self):
        if self.id in self.persistant_content: # If supplied app id already has an entry
            log.info(f"Updating app id: {self.id}")
            del self.persistant_content[self.id] # Delete it
            self.persistant_content.update(self.current_nonsteam_game) # and update it
        else:
            log.info(f"Adding app id: {self.id}")
            self.persistant_content.update(self.current_nonsteam_game) # Still add new entries

    def write_nonsteam(self):
        log.info("Writing to NonSteam.json")
        copy(self.nonsteam_path, f"{self.nonsteam_path}.bak") # Backup NonSteam.json incase file gets corrupted
        with open(self.nonsteam_path, "w", encoding="UTF-8") as out:
            json.dump(self.persistant_content, out)

    def update_installed_games(self, f_handler):
        #Add non steam id and unix timestamp to the completed dictionary, allowing them to be compared with steam games.
        f_handler.installed_games.update(self.persistant_content)