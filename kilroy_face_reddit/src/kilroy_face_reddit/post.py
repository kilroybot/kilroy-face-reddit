from typing import Optional
from uuid import UUID

from asyncpraw.models import Submission
from kilroy_face_py_shared import SerializableModel
from kilroy_server_py_utils import base64_encode

from kilroy_face_reddit.utils import download_image, get_filename_from_url


class PostTextData(SerializableModel):
    content: str


class PostImageData(SerializableModel):
    raw: str
    filename: Optional[str]


class PostData(SerializableModel):
    text: Optional[PostTextData]
    image: Optional[PostImageData]


class Post(SerializableModel):
    data: PostData
    id: UUID
    url: str

    @classmethod
    async def from_submission(cls, submission: Submission) -> "Post":
        text = PostTextData(content=submission.title)
        image = None
        if not submission.is_self:
            image = PostImageData(
                raw=base64_encode(await download_image(submission.url)),
                filename=get_filename_from_url(submission.url),
            )
        return cls(
            data=PostData(text=text, image=image),
            id=UUID(int=int(submission.id, 36)),
            url="https://reddit.com" + submission.permalink,
        )
