from dataclasses import dataclass
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Dict, Any, Type, Optional, AsyncIterable

from asyncpraw import Reddit
from asyncpraw.models import Submission
from kilroy_face_py_shared import SerializableModel
from kilroy_server_py_utils import (
    CategorizableBasedParameter,
    Configurable,
    Savable,
    classproperty,
)
from kilroy_server_py_utils.parameters.categorizable import CategorizableType

from kilroy_face_reddit.scraping.base import Scraper
from kilroy_face_reddit.scraping.frontpage.sorting import Sorting, HotSorting


class Params(SerializableModel):
    sorting: str = "hot"
    sortings_params: Dict[str, Dict[str, Any]] = {}


@dataclass
class State:
    sorting: Sorting
    sortings_params: Dict[str, Dict[str, Any]]


class FrontpageScraper(Scraper, Configurable[State]):
    class SortingParameter(CategorizableBasedParameter[State, Sorting]):
        # noinspection PyMethodParameters
        @classproperty
        def default_categorizable(cls) -> Type[CategorizableType]:
            return HotSorting

    @classmethod
    async def _build_sorting(cls, params: Params) -> Sorting:
        return await cls._build_generic(
            Sorting,
            category=params.sorting,
            **params.sortings_params.get(params.sorting, {}),
        )

    async def _build_default_state(self) -> State:
        params = Params(**self._kwargs)
        return State(
            sorting=await self._build_sorting(params),
            sortings_params=params.sortings_params,
        )

    @classmethod
    async def _save_state(cls, state: State, directory: Path) -> None:
        if isinstance(state.sorting, Savable):
            await state.sorting.save(directory / "sorting")

        state_dict = {
            "sorting_type": state.sorting.category,
            "sortings_params": state.sortings_params,
        }
        await cls._save_state_dict(state_dict, directory)

    @classmethod
    async def _load_sorting(
        cls, state_dict: Dict[str, Any], params: Params, directory: Path
    ) -> Sorting:
        category = state_dict.get("sorting_type", params.sorting)
        return await cls._load_generic(
            directory,
            Sorting,
            category=category,
            **state_dict.get("sortings_params", {}).get(category, {}),
            default=partial(cls._build_sorting, params),
        )

    async def _load_saved_state(self, directory: Path) -> State:
        params = Params(**self._kwargs)
        state_dict = await self._load_state_dict(directory)
        return State(
            sorting=await self._load_sorting(
                state_dict, params, directory / "sorting"
            ),
            sortings_params=state_dict.get(
                "sortings_params", params.sortings_params
            ),
        )

    async def cleanup(self) -> None:
        async with self.state.write_lock() as state:
            if isinstance(state.sorting, Configurable):
                await state.sorting.cleanup()

    async def scrap(
        self,
        client: Reddit,
        before: Optional[datetime] = None,
        after: Optional[datetime] = None,
    ) -> AsyncIterable[Submission]:
        async with self.state.read_lock() as state:
            sorting = state.sorting

        me = await client.user.me()

        async for submission in sorting.get(client.front):
            if (
                before is not None
                and submission.created_utc > before.timestamp()
            ):
                continue
            if (
                after is not None
                and submission.created_utc < after.timestamp()
            ):
                continue

            if (
                submission.author is not None
                and submission.author.name == me.name
            ):
                continue

            yield submission
