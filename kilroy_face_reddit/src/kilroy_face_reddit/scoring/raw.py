from abc import ABC, abstractmethod

from asyncpraw.models import Submission
from kilroy_face_server_py_sdk import Categorizable, classproperty, normalize


class Scorer(Categorizable, ABC):
    # noinspection PyMethodParameters
    @classproperty
    def category(cls) -> str:
        name: str = cls.__name__
        return normalize(name.removesuffix("Scorer"))

    @abstractmethod
    async def score(self, post: Submission) -> float:
        pass


# Reactions


class RelativeScoreScorer(Scorer):
    async def score(self, post: Submission) -> float:
        score = post.score
        if hasattr(post, "subreddit_subscribers"):
            subscribers = post.subreddit_subscribers
        else:
            if not hasattr(post.subreddit, "subscribers"):
                await post.subreddit.load()
            subscribers = post.subreddit.subscribers
        return score / max(subscribers, 1)
