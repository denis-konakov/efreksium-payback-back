import asyncio
import functools
import inspect
from contextlib import contextmanager
from functools import update_wrapper, partial, wraps
from typing import Iterable, Callable, Type, Any

from .response import ResponseException, HTTPResponseModel


class ThrowableFunction:
    def __init__(self, f: Callable, exceptions=None):
        self._function = f
        self._exceptions: list[Type[ResponseException]] = exceptions or []
        update_wrapper(self, f)
    def __repr__(self):
        return f'<{self.__class__.__name__} exceptions={self._exceptions} function={self._function}>'
    def __call__(self, *args, **kwargs):
        return self._function(*args, **kwargs)
    def __get__(self, instance: Callable, owner: Type[Callable]):
        return partial(self.__call__, instance)
    def name(self) -> str:
        return self._function.__name__

    def exceptions(self):
        return self._exceptions[:]

    def __getattr__(self, item):
        return getattr(self._function, item)


class ThrowableAsyncFunction(ThrowableFunction):
    async def __call__(self, *args, **kwargs):
        return await self._function(*args, **kwargs)


class ThrowableContextManager(ThrowableFunction):
    def __init__(self, f: Callable, exceptions=None):
        super().__init__(contextmanager(f), exceptions)

    def __call__(self, *args, **kwargs):
        with self._function(*args, **kwargs) as t:
            yield t


Throwable = ThrowableFunction | ThrowableContextManager
ThrowsExceptionsList = Iterable[ThrowableFunction | Type[ResponseException]]


class ThrowsManager:
    def __init__(self):
        pass

    @classmethod
    def get_base(cls,
                 t: Callable
                 ) -> Type[ThrowableFunction]:
        if inspect.isgeneratorfunction(t):
            return ThrowableContextManager
        if asyncio.iscoroutinefunction(t):
            return ThrowableAsyncFunction
        return ThrowableFunction

    @classmethod
    def join(cls, exceptions: ThrowsExceptionsList) -> list[Type[ResponseException]]:
        r = set()
        for i in exceptions:
            t = set()
            if isinstance(i, functools.partial):
                i = i.func.__self__
            if hasattr(i, 'exceptions'):
                t = set(cls.join(i.exceptions()))
            elif inspect.isclass(i) and issubclass(i, ResponseException):
                t = {i}
            else:
                raise ValueError('Unsupported type ' + i.__class__.__name__)
            r |= t
        return list(r)

    @classmethod
    def docs(cls, exceptions: ThrowsExceptionsList) -> dict[int, dict]:
        exceptions = cls.join(exceptions)
        r = {}
        for i in exceptions:
            if i.status_code() not in r:
                if i.META.get('response', None) is not None:
                    r[i.status_code()] = {
                        'description': i.detail(),
                        'model': HTTPResponseModel[i.META.get('response')]
                    }
                    continue
                r[i.status_code()] = {
                    'description': f'Ответ с кодом {i.status_code()}',
                    'content': {'application/json': {'examples': {}}},
                    'model': HTTPResponseModel[type(None)],
                }
            r[i.status_code()]['content']['application/json']['examples'][i.detail()] = i.example()
        return r
    def __call__(self,
                 exceptions: ThrowsExceptionsList | Callable | None = None
                 ) -> ThrowableFunction | Callable[[...], ThrowableFunction]:
        if callable(exceptions):
            return self.get_base(exceptions)(exceptions)
        exceptions = exceptions or []
        r = self.join(exceptions)

        def throws_type_decorator(f: Callable[[], Any]):
            return self.get_base(f)(f, exceptions)

        return throws_type_decorator


throws = ThrowsManager()
