from typing import List

from tests.models import IBaseModelForUTest
from tests.models.with_basic_types import WithBasicTypes


class WithRepeatedFields(IBaseModelForUTest):
    repeated_string_field: List[str]
    repeated_structured_type_field: List[WithBasicTypes]

    @staticmethod
    def get_expected_protobuf() -> str:
        return """message WithRepeatedFields {
    repeated string repeated_string_field = 1;
    repeated WithBasicTypes repeated_structured_type_field = 2;
}
"""
