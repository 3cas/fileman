import os

VERSION = "2.0a"

VALID_KEYS = "abcdefghijklmnopqrstuvwxyz"
IMAGE_EXTS = ["png", "jpg", "jpeg", "heic", "heif", "webp", "gif"]

code_dir = os.path.dirname(__file__)
MAIN_DIR = os.path.dirname(code_dir)
LOG_DIR = os.path.join(MAIN_DIR, "logs")
CONF_PATH = os.path.join(MAIN_DIR, "fm_config.json")
LOGO_PATH = os.path.join(MAIN_DIR, "logo.png")

CONF_DEFAULT = {
    "version": VERSION,
    "home_dir": os.path.expanduser("~"),
    "log_enabled": True,
    "log_verbose": False,
    "recent_keysets": []
}



