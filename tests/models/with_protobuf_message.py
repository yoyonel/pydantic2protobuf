from typing import List

from pydantic import BaseModel, Field

from pydantic2protobuf.tools.from_pydantic import gen_extra_fields


class WithProtobufMessage(BaseModel):
    float_field: float
    integer_field: int
    manual_protobuf_message_field: List[List[int]] = Field(
        ...,
        description="",
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
