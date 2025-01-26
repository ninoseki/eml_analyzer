from typing import TypeVar, Union

T = TypeVar("T")

ListSet = Union[list[T], set[T]]  # noqa: UP007
