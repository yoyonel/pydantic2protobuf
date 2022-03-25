"""
https://www.python.org/dev/peps/pep-0557/#inheritance
"""
from abc import ABC
from dataclasses import InitVar, dataclass, field
from typing import Optional

from parametrization import Parametrization  # type: ignore


@dataclass
class IParametrizationCase(ABC):
    # https://stackoverflow.com/a/55796971
    name: Optional[str] = field(init=False)  # pytest case name
    name_init: InitVar[Optional[str]]

    def __post_init__(self, name_init: Optional[str]):
        if self.__class__ == IParametrizationCase:
            raise TypeError("Cannot instantiate abstract class.")  # pragma: no cover
        self.name = name_init
        if self.name == "":
            self.name = None

    def __iter__(self):
        return iter(self.__dict__.items())

    @classmethod
    def case(cls, parametrization_case):
        if not isinstance(parametrization_case, IParametrizationCase):
            raise TypeError(
                f"{parametrization_case} not an instance of abstract class: {IParametrizationCase}"
            )  # pragma: no cover
        return Parametrization.case(**dict(parametrization_case))
