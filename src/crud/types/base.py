from abc import ABC, abstractmethod
class AbstractTypeBase(ABC):
    @classmethod
    @abstractmethod
    def __get_validators__(cls): ...
    @classmethod
    @abstractmethod
    def __modify_schema__(cls, field_schema: dict): ...
