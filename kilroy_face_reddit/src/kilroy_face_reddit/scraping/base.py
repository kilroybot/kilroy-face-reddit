from abc import ABC, abstractmethod
from datetime import datetime
from typing import AsyncIterable, Optional

from asyncpraw import Reddit
from asyncpraw.models import Submission
from kilroy_face_server_py_sdk import Categorizable, classproperty, normalize


class Scraper(Categorizable, ABC):
    # noinspection PyMethodParameters
    @classproperty
    def category(cls) -> str:
        name: str = cls.__name__
        return normalize(name.removesuffix("Scraper"))

    @abstractmethod
    def scrap(
        self,
        client: Reddit,
        before: Optional[datetime] = None,
        after: Optional[datetime] = None,
    ) -> AsyncIterable[Submission]:
        pass
