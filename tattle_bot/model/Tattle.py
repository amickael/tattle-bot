import time
import logging

from praw import Reddit
from praw.exceptions import RedditAPIException
from praw.models.reddit.comment import Comment
from praw.models.util import stream_generator

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
    def __process(
        handler: Activity,
        mention: Comment,
        retry: int = 5,
        cooldown: int = 30,
        buffer: int = 5,
    ):
        target_user = mention.parent().author
        message = handler.combined_formatted(target_user)
        for _ in range(retry + 1):
            try:
                mention.reply(message)
            except RedditAPIException as e:
                logging.error(e)
                multiplier = 1
                for error in e.items:
                    if error.field == "ratelimit":
                        error_message = error.error_message
                        try:
                            cooldown = int(
                                "".join([i for i in error_message if i.isdigit()])
                            )
                            if "minute" in error_message:
                                multiplier = 60
                        except ValueError:
                            pass
                        else:
                            break
                time.sleep(cooldown * multiplier + buffer)
            else:
                mention.mark_read()
                logging.info(
                    f"Fetched info about /u/{target_user} for /u/{mention.author}"
                )
                break

    def listen(self, skip_existing: bool = True):
        handler = Activity(self.client)
        for mention in stream_generator(
            self.client.inbox.mentions, skip_existing=skip_existing
        ):
            try:
                if isinstance(mention, Comment):
                    self.__process(handler, mention)
            except Exception as e:
                logging.error(e)
