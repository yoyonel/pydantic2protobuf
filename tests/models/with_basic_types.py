from pydantic import BaseModel, Field

from pydantic2protobuf.tools.from_pydantic import gen_extra_fields


class WithBasicTypes(BaseModel):
    __expected_proto__ = """message WithBasicTypes {
    float float_field = 1;
    int32 integer_field = 2;
    uint32 unsigned_integer_field = 3;
}
"""
    float_field: float
    integer_field: int
    unsigned_integer_field: int = Field(**gen_extra_fields(number=3, is_unsigned=True))
