from typing import List

from pydantic import BaseModel

from tests.models.with_basic_types import WithBasicTypes


class WithRepeatedFields(BaseModel):
    __expected_proto__ = """message WithRepeatedFields {
    repeated string repeated_string_field = 1;
    repeated WithBasicTypes repeated_structured_type_field = 2;
}
"""
    repeated_string_field: List[str]
    repeated_structured_type_field: List[WithBasicTypes]
