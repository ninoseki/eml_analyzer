import typing
from abc import ABC, abstractmethod


class AbstractFactory(ABC):
    @abstractmethod
    def call(self, *args: typing.Any, **kwargs: typing.Any):
        raise NotImplementedError()


class AbstractAsyncFactory(ABC):
    @abstractmethod
    async def call(self, *args: typing.Any, **kwargs: typing.Any):
        raise NotImplementedError()
