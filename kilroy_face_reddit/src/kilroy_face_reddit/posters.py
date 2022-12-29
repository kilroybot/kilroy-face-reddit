from abc import ABC, abstractmethod
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import UUID

from asyncpraw.models import Subreddit
from kilroy_server_py_utils import (
    Categorizable,
    classproperty,
    normalize,
    base64_decode,
)

from kilroy_face_reddit.post import PostData, Post


class Poster(Categorizable, ABC):
    # noinspection PyMethodParameters
    @classproperty
    def category(cls) -> str:
        name: str = cls.__name__
        return normalize(name.removesuffix("Poster"))

    @abstractmethod
    async def post(self, subreddit: Subreddit, data: PostData) -> Post:
        pass


# Basic


class BasicPoster(Poster):
    async def post(self, subreddit: Subreddit, data: PostData) -> Post:
        if data.image is None:
            submission = await subreddit.submit(
                title=data.text.content, selftext=""
            )
        else:
            with TemporaryDirectory() as tmpdir:
                tmpdir = Path(tmpdir)
                path = tmpdir / (data.image.filename or "image")
                with path.open("wb") as f:
                    f.write(base64_decode(data.image.raw))
                submission = await subreddit.submit_image(
                    title=data.text.content, image_path=str(path)
                )
        await submission.load()
        return Post(
            data=data,
            id=UUID(int=int(submission.id, 36)),
            url="https://reddit.com" + submission.permalink,
        )
