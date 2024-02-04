import typing
from abc import ABC, abstractmethod


class AbstractFactory(ABC):
    @classmethod
    @abstractmethod
    def call(cls, *args: typing.Any, **kwargs: typing.Any):
        raise NotImplementedError()


class AbstractAsyncFactory(ABC):
    @classmethod
    @abstractmethod
    async def call(cls, *args: typing.Any, **kwargs: typing.Any):
        raise NotImplementedError()
