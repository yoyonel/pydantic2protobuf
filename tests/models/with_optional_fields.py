from typing import Optional

from pydantic import BaseModel


class WithOptionalFields(BaseModel):
    __expected_proto__ = """message WithOptionalFields {
    google.protobuf.StringValue optional_string = 1;
    google.protobuf.UInt32Value optional_int = 2;
}
"""
    optional_string: Optional[str]
    optional_int: Optional[int]
