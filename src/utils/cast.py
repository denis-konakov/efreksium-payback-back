from typing import TypeVar, Any, Type

T = TypeVar('T')
def cast(obj: Any, __type: Type[T]) -> T:
    return obj
