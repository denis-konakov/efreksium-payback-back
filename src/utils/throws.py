import asyncio
import inspect
from contextlib import contextmanager
from functools import update_wrapper
from typing import Iterable, Callable, Type, Any, overload

from .response import ResponseException, HTTPResponseModel


class ThrowableFunction:
    def __init__(self, f: Callable):
        self._function = f
        self._exceptions: list[ResponseException] = []
        update_wrapper(self, f)

    def __call__(self, *args, **kwargs):
        return self._function(*args, **kwargs)

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
    def __init__(self, f: Callable):
        super().__init__(contextmanager(f))

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
                 ) -> Type[ThrowableFunction] | Type[ThrowableContextManager] | Type[ThrowableAsyncFunction]:
        if inspect.isgeneratorfunction(t):
            return ThrowableContextManager
        if asyncio.iscoroutinefunction(t):
            return ThrowableAsyncFunction
        return ThrowableFunction

    @classmethod
    def join(cls, exceptions: ThrowsExceptionsList) -> list[Type[ResponseException]]:
        r = set()
        for i in exceptions:
            if hasattr(i, 'exceptions'):
                r |= set(i.exceptions())
            elif inspect.isclass(i) and issubclass(i, ResponseException):
                r |= {i}
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
        if exceptions is None:
            exceptions = []
        r = self.join(exceptions)

        def wrapper(f: Callable[[], Any]):
            class Wrapper(self.get_base(f)):
                def __init__(self, func: Callable):
                    super().__init__(func)
                    self._exceptions = r

            return Wrapper(f)

        return wrapper


throws = ThrowsManager()
