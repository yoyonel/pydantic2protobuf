from typing import List

from pydantic import Field

from pydantic2protobuf.tools.from_pydantic import gen_extra_fields
from tests.models import IBaseModelForUTest


class WithProtobufMessage(IBaseModelForUTest):
    float_field: float
    integer_field: int
    manual_protobuf_message_field: List[List[int]] = Field(
        ...,
        description="""""",
        **gen_extra_fields(
            number=3,
            protobuf_message="""\
message WithProtobufMessageField {
    message TupleIds {
        uint32 id_a = 1;
        uint32 id_b = 2;
    }
    repeated TupleIds paired_ids = 1;
}
WithProtobufMessageField pairedIds = 3;""",
        ),
    )

    @staticmethod
    def _get_expected_protobuf() -> str:
        return """message WithProtobufMessage {
    float float_field = 1;
    int32 integer_field = 2;
    message WithProtobufMessageField {
        message TupleIds {
            uint32 id_a = 1;
            uint32 id_b = 2;
        }
        repeated TupleIds paired_ids = 1;
    }
    WithProtobufMessageField pairedIds = 3;
}
"""
