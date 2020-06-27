import os

from dotenv import load_dotenv

if os.path.isfile("../.env"):
    load_dotenv("../.env")

from tattle_bot.model import Tattle

########################################################################################################################
# Instantiate app
########################################################################################################################
with open("../VERSION", "r") as infile:
    VERSION = infile.read().strip()
client = Tattle(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=f"python:com.tattlebot.tattlebot:v{VERSION} (by u/Tattle_Bot)",
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
)

########################################################################################################################
# Run
########################################################################################################################
if __name__ == "__main__":
    client.listen()
