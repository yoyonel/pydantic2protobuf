from typing import Optional

from pydantic import BaseModel

from pydantic2protobuf.tools.pydantic_protobuf_types import UInt32Value


class WithOptionalFields(BaseModel):
    optional_string: Optional[str]
    optional_int: Optional[UInt32Value]


# if __name__ == "__main__":
#     pprint(WithOptionalFields().schema())
