import itertools
from collections import abc
from dataclasses import asdict, dataclass, field
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


@dataclass
class ProtoFieldsDefinition:
    number: int = field(default=1)

    protobuf_message: Optional[str] = field(default=None)
    allow_none: bool = field(default=True)
    is_unsigned: bool = field(default=False)
    disable_rpc: bool = field(default=False)

    def to_cls_properties(self):
        return {"extra": {"protobuf": asdict(self)}}

    @classmethod
    def from_cls_properties(cls, cls_properties: dict, default_number: int):
        try:
            json_proto_fields = cls_properties["extra"]["protobuf"]
        except KeyError:
            json_proto_fields = {"number": default_number}
        return cls(**json_proto_fields)


LIST_TYPES_ITERABLES = {list, List, Iterable, abc.Iterable}


class Chunkify(BaseModel):
    pass


def gen_extra_fields(
    number: int,
    protobuf_message: Optional[str] = None,
    allow_none: bool = True,
    is_unsigned: bool = False,
    disable_rpc: bool = False,
) -> Dict:
    return ProtoFieldsDefinition(
        number=number,
        protobuf_message=protobuf_message,
        allow_none=allow_none,
        is_unsigned=is_unsigned,
        disable_rpc=disable_rpc,
    ).to_cls_properties()


def extract_proto_fields(cls_properties: Dict, default_number: int) -> ProtoFieldsDefinition:
    return ProtoFieldsDefinition.from_cls_properties(cls_properties, default_number)


def is_type_iterable(outer_type: Any) -> bool:
    return getattr(outer_type, "__origin__", None) in LIST_TYPES_ITERABLES or issubclass(outer_type, Chunkify)


def extract_model_meta_classes(model_meta_class: Any) -> Iterator[Type[ModelMetaclass]]:
    model_fields: Iterable[ModelField] = model_meta_class.__fields__.values()
    # TODO: remove recurrence
    model_meta_classes = [
        extract_model_meta_classes(model_field.type_)
        for model_field in filter(lambda mf: isinstance(mf.type_, ModelMetaclass), model_fields)
    ]
    return itertools.chain(
        *(
            *(
                [
                    model_meta_class,
                ],
            ),
            *model_meta_classes,
        )
    )
