from typing import Self, Any, Callable, Type, Iterable


class ErrorHandleContext:
    def __init__(self, owner: Any):
        self.__owner = owner
        self.__error: list[Exception] = []
    def __bool__(self):
        return len(self.__error) == 0
    def __call__(self, error: Exception | None = None):
        if error is None:
            return
        self.__error.append(error)
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


class ErrorHandleProxy:
    def __init__(self, obj: type | Callable, context: ErrorHandleContext):
        self.__value = obj
        self.__context = context
    @property
    def value(self):
        return self.__value
    def __getattr__(self, item):
        while isinstance(self.__value, ErrorHandleProxy):
            self.__value = self.__value.value
        r = getattr(self.__value, item)
        return ErrorHandleProxy(r, self.__context)
    def __call__(self, *args, **kwargs) -> tuple[Any | None, Exception | None]:
        try:
            return self.__value(*args, **kwargs)
        except Exception as e:
            self.__context.add(e)
            return None


class CRUDBase:
    @classmethod
    def handled(cls, context: ErrorHandleContext) -> Self:
        t: cls = ErrorHandleProxy(cls, context)
        return t
    @classmethod
    def error(cls):
        return ErrorHandleContext(cls)
    @classmethod
    def ctx(cls):
        return ErrorHandleContext(cls)
