from pydantic import BaseModel
from typing_extensions import Type

from pydantic2protobuf.tools.to_proto import (
    PYTHON_TO_GOOGLE_PROTOBUF_TYPES,
    PYTHON_TO_PROTOBUF_TYPES,
    extract_proto_fields,
    is_type_iterable,
)


def pydantic_to_proto(base_model: Type[BaseModel], indent_level: int = 0, prefix_name: str = "") -> str:
    cls_properties = base_model.schema()["properties"]

    def _add_repeated(field_) -> str:
        return "repeated " if is_type_iterable(field_) else ""

    def _get_protobuf_type(field_, proto_fields) -> str:
        map_python_to_proto = PYTHON_TO_PROTOBUF_TYPES
        if proto_fields["allow_none"] and field_.allow_none:
            map_python_to_proto = PYTHON_TO_GOOGLE_PROTOBUF_TYPES
        return map_python_to_proto.get(field_.type_) or field_.type_.__name__

    def gen_protobuf_message(field_, enumerate_number: int) -> str:
        proto_fields = extract_proto_fields(cls_properties[field_.name], default_number=enumerate_number)
        if proto_fields["protobuf_message"]:
            return proto_fields["protobuf_message"]
        return "".join(
            f"{' ' * 4}"
            f"{'// disabled: ' if proto_fields.get('disable_rpc', False) else ''}"
            f"{_add_repeated(field_.outer_type_)}"
            f"{'u' if proto_fields['is_unsigned'] else ''}{_get_protobuf_type(field_, proto_fields)} "
            f"{field_.name} = {proto_fields['number']};"
        )

    return "\n".join(
        f"{' ' * 4 * indent_level}{proto_msg_line}"
        for proto_msg_line in [
            # message definition
            f"message {prefix_name}{base_model.__name__} {{",
            # TODO: need to test and understand the use case
            # inner classes/messages
            # *[inner_class.to_proto(indent_level=indent_level + 1)
            #   for inner_class in [c for c in vars(base_model).values() if isinstance(c, type(base_model))]],
            # messages sentences/lines from pydantic fields
            *[
                gen_protobuf_message(field_, default_number)
                for default_number, field_ in enumerate(base_model.__fields__.values(), start=1)
            ],
            "}",
        ]
    )
