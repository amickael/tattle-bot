import time

from praw import Reddit
from praw.exceptions import RedditAPIException
from praw.models.reddit.comment import Comment

from .Activity import Activity


class Tattle:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ):
        self.client = Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )

    def listen(self, skip_existing: bool = True):
        handler = Activity(self.client)
        for item in self.client.inbox.stream(skip_existing=skip_existing):
            if isinstance(item, Comment):
                author = item.parent().author
                message = handler.combined_formatted(author)
                while True:
                    try:
                        item.reply(message)
                    except RedditAPIException as e:
                        duration = 30
                        multiplier = 1
                        exception = str(e)
                        if "ratelimit" in e:
                            duration = int(
                                "".join([i for i in exception if i.isdigit()])
                            )
                            if "minutes" in exception:
                                multiplier = 60
                        print(duration * multiplier + 5)
                        time.sleep(duration * multiplier + 5)
                    else:
                        break
