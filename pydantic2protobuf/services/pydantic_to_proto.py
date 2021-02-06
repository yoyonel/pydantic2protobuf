from pydantic.fields import ModelField
from pydantic.main import BaseModel, ModelMetaclass

from pydantic2protobuf.tools.format import new_line, tab
from pydantic2protobuf.tools.from_pydantic import (
    PythonToGoogleProtoBufTypes,
    PythonToProtoBufTypes,
    extract_proto_fields,
    is_type_iterable,
)


def add_repeated_qualifier(field: ModelField) -> str:
    """"""
    return "repeated " if is_type_iterable(field) else ""


def translate_type(field: ModelField, proto_fields: dict) -> str:
    """"""
    return (
        PythonToGoogleProtoBufTypes if proto_fields.get("allow_none") and field.allow_none else PythonToProtoBufTypes
    ).get(field.type_) or field.type_.__qualname__


def gen_fields_definitions(base_model: BaseModel):
    cls_properties = base_model.schema()["properties"]

    def _gen_field_definition(field: ModelField, enumerate_number: int) -> str:
        proto_fields = extract_proto_fields(cls_properties[field.name], default_number=enumerate_number)
        if proto_fields.get("protobuf_message"):
            return proto_fields["protobuf_message"]
        return "".join(
            f"{tab}{'// disabled: ' if proto_fields.get('disable_rpc') else ''}"
            f"{add_repeated_qualifier(field.outer_type_)}"
            f"{'u' if proto_fields.get('is_unsigned') else ''}{translate_type(field, proto_fields)} "
            f"{field.name} = {proto_fields.get('number')};"
        )

    return [
        _gen_field_definition(field, default_number)
        for default_number, field in enumerate(base_model.__fields__.values(), start=1)
    ]


def gen_message_definition(base_model, indent_level: int = 0, prefix_name: str = "") -> str:
    pydantic_base_model: BaseModel = base_model
    pydantic_model_meta_class: ModelMetaclass = base_model
    return new_line.join(
        f"{tab * indent_level}{proto_msg_line}"
        for proto_msg_line in [
            f"message {prefix_name}{pydantic_model_meta_class.__qualname__} {{",
            *gen_fields_definitions(pydantic_base_model),
            f"}}{new_line}",
        ]
    )
