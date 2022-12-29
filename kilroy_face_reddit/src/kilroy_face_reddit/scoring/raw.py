from abc import ABC, abstractmethod

from kilroy_face_server_py_sdk import Categorizable, classproperty, normalize
from asyncpraw.models import Submission


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


class ScoreScorer(Scorer):
    async def score(self, post: Submission) -> float:
        return post.score
