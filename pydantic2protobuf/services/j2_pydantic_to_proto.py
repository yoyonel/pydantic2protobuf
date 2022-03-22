from dataclasses import dataclass
from typing import Dict, List, Optional

from pydantic.fields import ModelField
from pydantic.main import BaseModel, ModelMetaclass

from pydantic2protobuf.tools.from_pydantic import (
    PythonToGoogleProtoBufTypes,
    PythonToProtoBufTypes,
    extract_proto_fields,
    is_type_iterable,
)


@dataclass(frozen=True)
class FieldDefinition:
    field_name: str
    type_translated: str

    disable_rpc: bool
    is_iterable: bool
    is_unsigned: bool
    field_number: int

    proto_message: Optional[str]


@dataclass(frozen=True)
class MessageDefinition:
    name: str
    fields: list[FieldDefinition]


def translate_type(field: ModelField, proto_fields: dict) -> str:
    field_allow_none = bool(proto_fields.get("allow_none") and field.allow_none)
    map_for_types = (PythonToProtoBufTypes, PythonToGoogleProtoBufTypes)[field_allow_none]
    return map_for_types.get(field.type_) or field.type_.__qualname__


def gen_field_definition(field: ModelField, field_properties: Dict, enumerate_number: int) -> FieldDefinition:
    proto_fields = extract_proto_fields(field_properties, default_number=enumerate_number)
    return FieldDefinition(
        proto_message=proto_fields.get("protobuf_message"),
        disable_rpc=proto_fields["disable_rpc"],
        is_iterable=is_type_iterable(field.outer_type_),
        is_unsigned=proto_fields["is_unsigned"],
        type_translated=translate_type(field, proto_fields),
        field_name=field.name,
        field_number=proto_fields["number"],
    )


def gen_fields_definitions(base_model: BaseModel) -> List[FieldDefinition]:
    cls_properties = base_model.schema()["properties"]
    return [
        gen_field_definition(field, cls_properties[field.name], default_number)
        for default_number, field in enumerate(base_model.__fields__.values(), start=1)
    ]


def gen_message_definition(base_model) -> MessageDefinition:
    pydantic_base_model: BaseModel = base_model
    pydantic_model_meta_class: ModelMetaclass = base_model
    return MessageDefinition(
        name=pydantic_model_meta_class.__qualname__, fields=gen_fields_definitions(pydantic_base_model)
    )
