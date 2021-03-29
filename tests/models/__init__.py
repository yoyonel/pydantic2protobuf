from abc import ABC, abstractmethod

from pydantic.main import BaseModel


class IBaseModelForUTest(BaseModel, ABC):
    @staticmethod
    @abstractmethod
    def _get_expected_protobuf() -> str:
        pass
