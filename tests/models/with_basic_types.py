from pydantic import BaseModel, PositiveInt


class WithBasicTypes(BaseModel):
    float_field: float
    integer_field: int
    unsigned_integer_field: PositiveInt
