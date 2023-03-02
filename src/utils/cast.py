from typing import TypeVar, Any

T = TypeVar('T')
def cast(obj: Any, __type: T) -> T:
    return obj
