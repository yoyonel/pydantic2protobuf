from pydantic.main import BaseModel, ModelMetaclass

from pydantic2protobuf.tools.format import new_line, tab
from pydantic2protobuf.tools.from_pydantic import (
    PYTHON_TO_GOOGLE_PROTOBUF_TYPES,
    PYTHON_TO_PROTOBUF_TYPES,
    extract_proto_fields,
    is_type_iterable,
)


def pydantic_to_proto(base_model, indent_level: int = 0, prefix_name: str = "") -> str:
    """"""
    pydantic_base_model: BaseModel = base_model
    cls_properties = pydantic_base_model.schema()["properties"]

    def _add_repeated_qualifier(field_) -> str:
        return "repeated " if is_type_iterable(field_) else ""

    def _get_protobuf_type(field_, proto_fields) -> str:
        """"""
        map_python_to_proto = (
            PYTHON_TO_GOOGLE_PROTOBUF_TYPES
            if proto_fields["allow_none"] and field_.allow_none
            else PYTHON_TO_PROTOBUF_TYPES
        )
        return map_python_to_proto.get(field_.type_) or field_.type_.__name__

    def gen_protobuf_message(field_, enumerate_number: int) -> str:
        """"""
        proto_fields = extract_proto_fields(cls_properties[field_.name], default_number=enumerate_number)
        if proto_fields["protobuf_message"]:
            return proto_fields["protobuf_message"]
        return "".join(
            f"{tab}{'// disabled: ' if proto_fields.get('disable_rpc', False) else ''}"
            f"{_add_repeated_qualifier(field_.outer_type_)}"
            f"{'u' if proto_fields['is_unsigned'] else ''}{_get_protobuf_type(field_, proto_fields)} "
            f"{field_.name} = {proto_fields['number']};"
        )

    pydantic_model_meta_class: ModelMetaclass = base_model
    return new_line.join(
        f"{tab * indent_level}{proto_msg_line}"
        for proto_msg_line in [
            f"message {prefix_name}{pydantic_model_meta_class.__qualname__} {{",
            *[
                gen_protobuf_message(field_, default_number)
                for default_number, field_ in enumerate(pydantic_base_model.__fields__.values(), start=1)
            ],
            f"}}{new_line}",
        ]
    )
