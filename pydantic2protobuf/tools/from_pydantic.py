from collections import abc
from typing import Any, ByteString, Dict, Iterable, List, NewType, Optional, Type, TypeVar

from pydantic import BaseModel
from pydantic.fields import ModelField
from pydantic.main import ModelMetaclass

uint32 = NewType("uint32", int)

T = TypeVar("T")

PYTHON_TO_PROTOBUF_TYPES: Dict[Any, str] = {
    bool: "bool",
    bytes: "str",
    ByteString: "str",
    float: "float",
    int: "int32",
    str: "string",
    Dict: "google.protobuf.Struct",
    uint32: "uint32",
}
PYTHON_TO_GOOGLE_PROTOBUF_TYPES: Dict[Any, str] = {
    bool: "google.protobuf.BoolValue",
    bytes: "google.protobuf.StringValue",
    ByteString: "google.protobuf.StringValue",
    float: "google.protobuf.FloatValue",
    int: "google.protobuf.UInt32Value",
    str: "google.protobuf.StringValue",
}


class Chunkify(BaseModel):
    pass


def proto_field(
    number: int,
    protobuf_message: Optional[str] = None,
    allow_none: bool = True,
    is_unsigned: bool = False,
    disable_rpc: bool = False,
) -> Dict:
    """

    :param number:
    :param protobuf_message:
    :param allow_none:
    :param is_unsigned:
    :param disable_rpc:
    :return:
    """
    return {
        "extra": {
            "proto": {
                "number": number,
                "protobuf_message": protobuf_message,
                "allow_none": allow_none,
                "is_unsigned": is_unsigned,
                "disable_rpc": disable_rpc,
            }
        }
    }


def extract_proto_fields(properties: Dict, default_number: int) -> Dict:
    """

    :param properties:
    :param default_number:
    :return:
    """
    return {
        **{
            "number": default_number,
            "protobuf_message": None,
            "allow_none": True,
            "is_unsigned": False,
            "disable_rpc": False,
        },
        **properties.get("extra", {}).get("proto", {}),
    }


def is_type_iterable(field_: Type[T]) -> bool:
    """

    :param field_:
    :return:
    """
    return getattr(field_, "__origin__", None) in {list, List, Iterable, abc.Iterable} or issubclass(field_, Chunkify)


def extract_model_meta_classes(model_meta_class) -> List[Type[ModelMetaclass]]:
    """

    :param model_meta_class:
    :return:
    """
    results: List[Type[ModelMetaclass]] = [model_meta_class]
    model_fields: Iterable[ModelField] = model_meta_class.__fields__.values()
    for model_field in model_fields:
        if isinstance(model_field.type_, ModelMetaclass):
            results.extend(extract_model_meta_classes(model_field.type_))
    return results
