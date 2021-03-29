from pydantic import PositiveInt

from tests.models import IBaseModelForUTest


class WithBasicTypes(IBaseModelForUTest):
    float_field: float
    integer_field: int
    unsigned_integer_field: PositiveInt

    @staticmethod
    def _get_expected_protobuf():
        return """message WithBasicTypes {
    float float_field = 1;
    int32 integer_field = 2;
    uint32 unsigned_integer_field = 3;
}
"""
