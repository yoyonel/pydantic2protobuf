import itertools
from collections import abc
from typing import Any, ByteString, Dict, Iterable, Iterator, List, Optional, Type

from pydantic import BaseModel, PositiveInt
from pydantic.fields import ModelField
from pydantic.main import ModelMetaclass

from pydantic2protobuf.tools.pydantic_protobuf_types import UInt32Value

PythonToProtoBufTypes: Dict[Any, str] = {
    bool: "bool",
    bytes: "str",
    ByteString: "str",
    float: "float",
    int: "int32",
    str: "string",
    Dict: "google.protobuf.Struct",
    # https://pydantic-docs.helpmanual.io/usage/types/
    PositiveInt: "uint32",
}

PythonToGoogleProtoBufTypes: Dict[Any, str] = {
    bool: "google.protobuf.BoolValue",
    bytes: "google.protobuf.StringValue",
    ByteString: "google.protobuf.StringValue",
    float: "google.protobuf.FloatValue",
    int: "google.protobuf.Int64Value",
    UInt32Value: "google.protobuf.UInt32Value",
    str: "google.protobuf.StringValue",
}

DEFAULT_DICT_FOR_PROTO_FIELDS = {
    "protobuf_message": None,
    "allow_none": True,
    "is_unsigned": False,
    "disable_rpc": False,
}


class Chunkify(BaseModel):
    pass


def gen_extra_fields(
    number: int,
    protobuf_message: Optional[str] = None,
    allow_none: bool = True,
    is_unsigned: bool = False,
    disable_rpc: bool = False,
) -> Dict:
    """"""
    return {
        "extra": {
            "protobuf": {
                "number": number,
                "protobuf_message": protobuf_message,
                "allow_none": allow_none,
                "is_unsigned": is_unsigned,
                "disable_rpc": disable_rpc,
            }
        }
    }


def extract_proto_fields(cls_properties: Dict, default_number: int) -> Dict:
    """"""
    return {
        **DEFAULT_DICT_FOR_PROTO_FIELDS,
        **{"number": default_number},
        **cls_properties.get("extra", {}).get("protobuf", {}),
    }


def is_type_iterable(field: Any) -> bool:
    """"""
    return getattr(field, "__origin__", None) in {list, List, Iterable, abc.Iterable} or issubclass(field, Chunkify)


def extract_model_meta_classes(model_meta_class: Any) -> Iterator[Type[ModelMetaclass]]:
    """"""
    model_fields: Iterable[ModelField] = model_meta_class.__fields__.values()
    return itertools.chain(
        *(
            *([model_meta_class],),
            *(
                extract_model_meta_classes(model_field.type_)
                for model_field in filter(lambda mf: isinstance(mf.type_, ModelMetaclass), model_fields)
            ),
        )
    )
