import os
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

from dotenv import load_dotenv

if os.path.isfile("../.env"):
    load_dotenv("../.env")

from tattle_bot.model import Tattle


########################################################################################################################
# Setup
########################################################################################################################
os.chdir(os.path.dirname(__file__))
__appname__ = "tattle-bot"
if os.path.isfile("../VERSION"):
    with open("../VERSION", "r") as infile:
        VERSION = infile.read().strip()
else:
    VERSION = "1.0.0"


########################################################################################################################
# Logging
########################################################################################################################
log_root = {
    "darwin": os.path.join(os.getenv("HOME", ""), "Library", "Logs"),
    "linux": "/var/log",
    "win32": os.getenv("APPDATA", ""),
}
log_path = os.path.join(
    log_root.get(sys.platform, ""), __appname__, f"{__appname__}.log",
)
if not os.path.exists(os.path.dirname(log_path)):
    os.makedirs(os.path.dirname(log_path))

# Set root logger params
log_formatter = logging.Formatter("%(levelname)s : %(asctime)s : %(message)s")
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Set file logger params
file_handler = TimedRotatingFileHandler(log_path, when="d", interval=1, backupCount=14)
file_handler.setFormatter(log_formatter)
root_logger.addHandler(file_handler)

# Set stream logger params
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
root_logger.addHandler(console_handler)

########################################################################################################################
# Instantiate app
########################################################################################################################
client = Tattle(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=f"python:com.tattlebot.tattlebot:v{VERSION} (by u/Tattle_Bot)",
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
)


########################################################################################################################
# Main function
########################################################################################################################
def main():
    logging.info(f"Starting {__appname__} (v{VERSION})")
    try:
        client.listen()
    except KeyboardInterrupt:
        logging.info("Shutting down")
        raise SystemExit


########################################################################################################################
# Run
########################################################################################################################
if __name__ == "__main__":
    main()
