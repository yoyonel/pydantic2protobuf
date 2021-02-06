from typing import Optional

from pydantic2protobuf.tools.pydantic_protobuf_types import UInt32Value
from tests.models import IBaseModelForUTest


class WithOptionalFields(IBaseModelForUTest):
    optional_string: Optional[str]
    optional_int: Optional[UInt32Value]

    @staticmethod
    def get_expected_protobuf():
        return """message WithOptionalFields {
    google.protobuf.StringValue optional_string = 1;
    google.protobuf.UInt32Value optional_int = 2;
}
"""


if __name__ == "__main__":
    print(WithOptionalFields().schema())
