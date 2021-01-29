from collections import abc
from typing import Any, ByteString, Dict, Iterable, List, NewType, Optional, Set, Type, TypeVar

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
    return getattr(field_, "__origin__", None) in (list, List, Iterable, abc.Iterable) or issubclass(field_, Chunkify)


def extract_all_model_meta_classes(model_meta_class: ModelMetaclass) -> Set[ModelMetaclass]:
    results = {model_meta_class}
    # TODO: remove this mypy ignore ...
    model_fields: Iterable[ModelField] = model_meta_class.__fields__.values()  # type: ignore
    for model_field in model_fields:
        if isinstance(model_field.type_, ModelMetaclass):
            results.update(extract_all_model_meta_classes(model_field.type_))
    return results


def gen_all_proto_msg_from_routes(routes):
    all_model_meta_classes = set()
    for route in routes:
        # from request field
        request_body_params = route.dependant.body_params
        if request_body_params:
            request_field = request_body_params[0]
            if request_field is not None and isinstance(request_field.type_, ModelMetaclass):
                all_model_meta_classes.update(extract_all_model_meta_classes(request_field.type_))
        # from response field
        response_field = route.response_field
        if response_field is not None and isinstance(response_field.type_, ModelMetaclass):
            all_model_meta_classes.update(extract_all_model_meta_classes(response_field.type_))
    return all_model_meta_classes
