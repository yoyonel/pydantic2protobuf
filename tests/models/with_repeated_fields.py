from typing import List

from pydantic import BaseModel

from tests.models.with_basic_types import WithBasicTypes


class WithRepeatedFields(BaseModel):
    repeated_string_field: List[str]
    repeated_structured_type_field: List[WithBasicTypes]
