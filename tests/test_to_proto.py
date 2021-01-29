from pydantic import BaseModel

from pydantic2protobuf.services.to_proto import pydantic_to_proto


class Model(BaseModel):
    a: float
    b: int = 10


def test_pydantic_to_proto():
    result_proto_msg = pydantic_to_proto(Model)
    expected_proto_msg = """message Model {
    float a = 1;
    int32 b = 2;
}"""
    assert result_proto_msg == expected_proto_msg
