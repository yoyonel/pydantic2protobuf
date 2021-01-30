from pydantic import BaseModel


class WithBasicTypes(BaseModel):
    __expected_proto__ = """message WithBasicTypes {
    float float_field = 1;
    int32 integer_field = 2;
}
"""
    float_field: float
    integer_field: int
