from typing import Dict, List

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
    field_allow_none = bool(proto_fields.get("allow_none") and field.allow_none)
    map_for_types = (PythonToProtoBufTypes, PythonToGoogleProtoBufTypes)[field_allow_none]
    return map_for_types.get(field.type_) or field.type_.__qualname__


def gen_field_definition(field: ModelField, field_properties: Dict, enumerate_number: int) -> str:
    proto_fields = extract_proto_fields(field_properties, default_number=enumerate_number)
    if proto_fields.get("protobuf_message"):
        return proto_fields["protobuf_message"]
    result = f"""{tab}{"// disabled: " if proto_fields.get("disable_rpc") else ""}"""
    result += f"{add_repeated_qualifier(field.outer_type_)}"
    result += f"""{"u" if proto_fields.get("is_unsigned") else ""}{translate_type(field, proto_fields)} """
    result += f"""{field.name} = {proto_fields.get("number")};"""
    return result


def gen_fields_definitions(base_model: BaseModel) -> List[str]:
    cls_properties = base_model.schema()["properties"]
    return [
        gen_field_definition(field, cls_properties[field.name], default_number)
        for default_number, field in enumerate(base_model.__fields__.values(), start=1)
    ]


def add_new_lines_and_indentation(lines: List[str], indent_level: int) -> str:
    return new_line.join(f"{tab * indent_level}{line}" for line in lines)


def gen_message_definition(base_model, indent_level: int = 0, prefix_name: str = "") -> str:
    pydantic_base_model: BaseModel = base_model
    pydantic_model_meta_class: ModelMetaclass = base_model
    message_definitions_lines = [
        f"message {prefix_name}{pydantic_model_meta_class.__qualname__} {{",
        *gen_fields_definitions(pydantic_base_model),
        f"}}{new_line}",
    ]
    return add_new_lines_and_indentation(message_definitions_lines, indent_level)
