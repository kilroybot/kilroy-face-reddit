from abc import ABC, abstractmethod
from typing import AsyncIterable, Literal, Dict, Any

from asyncpraw.models import Front, Submission
from kilroy_face_server_py_sdk import SerializableState
from kilroy_server_py_utils import (
    Categorizable,
    classproperty,
    normalize,
    Configurable,
    Parameter,
)

FILTERS = {"all", "day", "hour", "month", "week", "year"}
FiltersType = Literal["all", "day", "hour", "month", "week", "year"]


class Sorting(Categorizable, ABC):
    # noinspection PyMethodParameters
    @classproperty
    def category(cls) -> str:
        name: str = cls.__name__
        return normalize(name.removesuffix("Sorting"))

    @abstractmethod
    def get(self, front: Front) -> AsyncIterable[Submission]:
        pass


# Best


class BestSorting(Sorting):
    def get(self, front: Front) -> AsyncIterable[Submission]:
        return front.best(limit=None)  # type: ignore


# Controversial


class ControversialSortingState(SerializableState):
    filter: FiltersType = "all"


class ControversialSorting(Sorting, Configurable[ControversialSortingState]):
    class FilterParameter(Parameter[ControversialSortingState, str]):
        # noinspection PyMethodParameters
        @classproperty
        def schema(cls) -> Dict[str, Any]:
            return {
                "oneOf": [
                    {
                        "type": "string",
                        "title": filter_.capitalize(),
                        "const": filter_,
                        "default": filter_,
                        "readOnly": True,
                    }
                    for filter_ in FILTERS
                ],
                "type": "string",
                "title": cls.pretty_name,
                "default": "all",
            }

    async def get(self, front: Front) -> AsyncIterable[Submission]:
        async with self.state.read_lock() as state:
            filter_ = state.filter

        async for submission in front.controversial(
            filter=filter_, limit=None  # type: ignore
        ):
            yield submission


# Hot


class HotSorting(Sorting):
    def get(self, front: Front) -> AsyncIterable[Submission]:
        return front.hot(limit=None)  # type: ignore


# New


class NewSorting(Sorting):
    def get(self, front: Front) -> AsyncIterable[Submission]:
        return front.new(limit=None)  # type: ignore


# Random Rising


class RandomRisingSorting(Sorting):
    def get(self, front: Front) -> AsyncIterable[Submission]:
        return front.random_rising(limit=None)  # type: ignore


# Rising


class RisingSorting(Sorting):
    def get(self, front: Front) -> AsyncIterable[Submission]:
        return front.rising(limit=None)  # type: ignore


# Top


class TopSortingState(SerializableState):
    filter: FiltersType = "all"


class TopSorting(Sorting, Configurable[TopSortingState]):
    class FilterParameter(Parameter[TopSortingState, str]):
        # noinspection PyMethodParameters
        @classproperty
        def schema(cls) -> Dict[str, Any]:
            return {
                "oneOf": [
                    {
                        "type": "string",
                        "title": filter_.capitalize(),
                        "const": filter_,
                        "default": filter_,
                        "readOnly": True,
                    }
                    for filter_ in FILTERS
                ],
                "type": "string",
                "title": cls.pretty_name,
                "default": "all",
            }

    async def get(self, front: Front) -> AsyncIterable[Submission]:
        async with self.state.read_lock() as state:
            filter_ = state.filter

        async for submission in front.top(
            filter=filter_, limit=None  # type: ignore
        ):
            yield submission
