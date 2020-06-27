from collections import Counter

from praw import Reddit
from psaw import PushshiftAPI


class Activity:
    def __init__(self, reddit: Reddit):
        self.reddit = reddit
        self.api = PushshiftAPI(reddit)

    def combined(self, username: str, limit: int = 5) -> Counter:
        activity = self.api.redditor_subreddit_activity(username)
        counts = activity.get("comment", Counter([]))
        counts.update(activity.get("submission", Counter([])))
        return counts.most_common(limit)

    def combined_formatted(self, username: str, limit: int = 5) -> str:
        data = self.combined(username, limit)
        output = [
            f"Here are the top 5 most active subreddits for /u/{username}:",
            "",
            "Subreddit | Total activity",
            "---|:---:",
        ]
        try:
            output.extend([f"/r/{subreddit} | {count:,}" for subreddit, count in data])
        except ValueError:
            output.extend([f"/r/{subreddit} | {count}" for subreddit, count in data])
        output.extend(
            ["&nbsp;", "> I am a bot, this action was performed automatically"]
        )
        return "\n".join(output)
