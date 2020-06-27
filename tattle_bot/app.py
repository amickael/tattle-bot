import os
import logging
import sys
import datetime as dt

from dotenv import load_dotenv

if os.path.isfile("../.env"):
    load_dotenv("../.env")

from tattle_bot.model import Tattle


########################################################################################################################
# Setup
########################################################################################################################
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
    log_root.get(sys.platform, ""),
    __appname__,
    f"{__appname__} {dt.datetime.now().isoformat()}.log",
)
if not os.path.exists(os.path.dirname(log_path)):
    os.makedirs(os.path.dirname(log_path))

logging.basicConfig(
    format="%(levelname)s : %(asctime)s : %(message)s",
    level=logging.INFO,
    filename=log_path,
)

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
    logging.info("Starting application")
    client.listen()


########################################################################################################################
# Run
########################################################################################################################
if __name__ == "__main__":
    main()
