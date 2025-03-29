from datetime import datetime
import os
import json

from constants import LOG_DIR, CONF_PATH, CONF_DEFAULT

RUN_TIME = datetime.now().strftime("%Y%m%d_%H%M%S")

LOG_NAME = f"{RUN_TIME}.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_NAME)

# check for config file and log directory
if not os.path.isfile(CONF_PATH):
    with open(CONF_PATH, "w") as f:
        json.dump(CONF_DEFAULT, f, indent=4)
        CONF_LOADED = CONF_DEFAULT
else:
    with open(CONF_PATH, "r") as f:
        CONF_LOADED = json.load(f)

LOG_ENABLED = CONF_LOADED["log_enabled"]
LOG_VERBOSE = CONF_LOADED["log_verbose"]

if LOG_ENABLED:
    if not os.path.isdir(LOG_DIR):
        os.mkdir(LOG_DIR)

# set up logging
def log(message: str, verbose_only: bool = False):
    if LOG_ENABLED and (not verbose_only or LOG_VERBOSE):
        time = datetime.now().strftime("%H:%M:%S")
        with open(LOG_PATH, "a") as f:
            f.write(f"[{time}] {message}\n")

log("Defined constants, initializing app...", True)

