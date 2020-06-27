import time
from typing import Union
import logging

from praw import Reddit
from praw.exceptions import RedditAPIException
from praw.models.reddit.comment import Comment
from praw.models.reddit.message import Message

from tattle_bot.model.Activity import Activity


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

    @staticmethod
    def __process(handler: Activity, item: Union[Comment, Message]):
        if isinstance(item, Comment):
            requester = item.author
            author = item.parent().author
            message = handler.combined_formatted(author)
            while True:
                try:
                    item.reply(message)
                except RedditAPIException as e:
                    # Log error
                    logging.error(e)

                    # Initialize duration, multiplier, and exception
                    duration = 30
                    multiplier = 1
                    exception = str(e)

                    # If error is a rate limit then wait the specified duration
                    if "ratelimit" in exception:
                        duration = int("".join([i for i in exception if i.isdigit()]))
                        if "minute" in exception:
                            multiplier = 60
                    time.sleep(duration * multiplier + 5)
                else:
                    logging.info(f"Fetched info about /u/{author} for /u/{requester}")
                    break

    def listen(self, skip_existing: bool = True):
        handler = Activity(self.client)
        for item in self.client.inbox.stream(skip_existing=skip_existing):
            try:
                self.__process(handler, item)
            except Exception as e:
                logging.error(e)
