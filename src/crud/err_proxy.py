from typing import Self, Any, Callable, Type, Iterable
from utils import cast
from abc import ABC, abstractmethod
ExceptionProxyType = dict[Type[Exception], Type[Exception]]

class ErrorHandleContext:
    def __init__(self, owner: Type, *, handle: bool = True, proxy: ExceptionProxyType | None = None):
        self.__owner = owner
        self.__error: list[Exception] = []
        self.__proxy: ExceptionProxyType = proxy or dict()
        self.__handle: bool = handle
    def set_proxy(self, v: ExceptionProxyType | None = None):
        self.__proxy = v or dict()
    def set_handle(self, v: bool):
        self.__handle = v

    def __bool__(self):
        return len(self.__error) == 0

    def __call__(self, error: Exception | None = None):
        if error is None:
            return
        for k, v in self.__proxy.items():
            if isinstance(error, k):
                error = v()
        self.__error.append(error)
        if not self.__handle:
            raise error

    def __len__(self):
        return len(self.__error)

    def __repr__(self):
        return f'<ErrorHandleContext {self.__owner}>'

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return iter(self.__error)

    def clear(self):
        self.__error = []

    def reset(self):
        self.__error = []

    def add(self, error: Exception | None):
        self.__call__(error)

    def pop(self) -> bool:
        n = self.__bool__()
        self.__error = []
        return n

    def has(self, *args: tuple[Type[Exception]], mode: Callable[[Iterable[bool]], bool] = any):
        if len(args) == 0:
            return not self.__bool__()

        def iter_contains():
            for i in args:
                t = False
                for j in self.__error:
                    if isinstance(j, i):
                        t = True
                        break
                yield t

        return mode(iter_contains())


class AbstractErrorHandleProxy(ABC):
    @classmethod
    @abstractmethod
    def handled(cls, context: ErrorHandleContext | None = None, *, handle: bool = True) -> Self: ...
    @classmethod
    @abstractmethod
    def proxy(cls, proxy: ExceptionProxyType, context: ErrorHandleContext | None = None) -> Self:  ...
    @classmethod
    @abstractmethod
    def error(cls) -> ErrorHandleContext: ...
    @classmethod
    @abstractmethod
    def ctx(cls, *, handle: bool = True, proxy: ExceptionProxyType | None = None) -> ErrorHandleContext: ...
class ErrorHandleProxy(AbstractErrorHandleProxy):
    def __init__(self, obj: type | Callable, context: ErrorHandleContext):
        self.__value = obj
        self.__context = context
    def handled(self, context: ErrorHandleContext | None = None, *, handle: bool = True) -> Self:
        return self
    def proxy(self, proxy: ExceptionProxyType, context: ErrorHandleContext | None = None) -> Self:
        self.__context.set_proxy(proxy)
        return self
    def value(self):
        return self.__value
    def context(self):
        return self.__context
    def ctx(self, **kwargs) -> ErrorHandleContext:
        return self.__context
    def error(self) -> ErrorHandleContext:
        return self.ctx()
    def __getattr__(self, item):
        while isinstance(self.__value, ErrorHandleProxy):
            self.__value = self.__value.value
        r = getattr(self.__value, item)
        return ErrorHandleProxy(r, self.__context)

    def __call__(self, *args, **kwargs):
        try:
            return self.__value(*args, **kwargs)
        except Exception as e:
            self.__context.add(e)
            return None
class CRUDBase(AbstractErrorHandleProxy):
    @classmethod
    def handled(cls, context: ErrorHandleContext | None = None, *, handle: bool = True) -> Self:
        if context is None:
            context = ErrorHandleContext(cls, handle=handle)
        t: cls = cast(ErrorHandleProxy(cls, context), cls)
        return t
    @classmethod
    def proxy(cls, proxy: ExceptionProxyType, context: ErrorHandleContext | None = None):
        n = cls.handled(context, handle=False)
        n.proxy(proxy)
        return n
    @classmethod
    def error(cls) -> ErrorHandleContext:
        return cls.ctx()

    @classmethod
    def ctx(cls, *, handle: bool = True, proxy: ExceptionProxyType | None = None) -> ErrorHandleContext:
        return ErrorHandleContext(cls, handle=handle, proxy=proxy)
