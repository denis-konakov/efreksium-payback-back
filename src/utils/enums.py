from typing import Generic, TypeVar

T = TypeVar('T')

class EnumGroup(Generic[T]):
    def __init__(self, *args: T):
        self.__values = args

    def __eq__(self, v: T):
        return v in self.__values

    def __ne__(self, other: T):
        return not (self == other)

    def __or__(self, other: 'EnumGroup[T]'):
        return EnumGroup(
            *(self.__values + other.__values)
        )


__all__ = (
    'EnumGroup',
)
