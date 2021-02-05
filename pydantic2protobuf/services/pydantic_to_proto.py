from pydantic.fields import ModelField
from pydantic.main import BaseModel, ModelMetaclass

from pydantic2protobuf.tools.format import new_line, tab
from pydantic2protobuf.tools.from_pydantic import (
    PYTHON_TO_GOOGLE_PROTOBUF_TYPES,
    PYTHON_TO_PROTOBUF_TYPES,
    extract_proto_fields,
    is_type_iterable,
)


def _add_repeated_qualifier(field_) -> str:
    """
    # TODO: move to pytest utests
    >>> from pydantic import create_model as create_pydantic_model
    >>> from typing import Optional, List
    >>> _add_repeated_qualifier(create_pydantic_model("", text=(Optional[str], None), __base__=BaseModel).__fields__["text"].outer_type_)
    ''
    >>> _add_repeated_qualifier(create_pydantic_model("", texts=(Optional[List[str]], None), __base__=BaseModel).__fields__["texts"].outer_type_)
    'repeated '
    """
    return "repeated " if is_type_iterable(field_) else ""


def _get_protobuf_type(field_: ModelField, proto_fields: dict) -> str:
    """
    # TODO: move to pytest utests
    >>> from pydantic import create_model as create_pydantic_model
    >>> from typing import Optional, List
    >>> from pydantic2protobuf.tools.from_pydantic import uint32

    >>> _get_protobuf_type(create_pydantic_model("", repeated_string_field=(List[str], None), __base__=BaseModel).__fields__["repeated_string_field"], \
                            {'number': 1, 'protobuf_message': None, 'allow_none': False, 'is_unsigned': True, 'disable_rpc': False})
    'string'
    >>> _get_protobuf_type(create_pydantic_model("", integer_field=(int, None), __base__=BaseModel).__fields__["integer_field"], \
                            {'number': 1, 'protobuf_message': None, 'allow_none': False, 'is_unsigned': True, 'disable_rpc': False})
    'int32'
    >>> _get_protobuf_type(create_pydantic_model("", optional_string_field=(Optional[str], None), __base__=BaseModel).__fields__["optional_string_field"], \
                            {'number': 1, 'protobuf_message': None, 'allow_none': True, 'is_unsigned': False, 'disable_rpc': False})
    'google.protobuf.StringValue'
    """
    return (
        PYTHON_TO_GOOGLE_PROTOBUF_TYPES
        if proto_fields.get("allow_none") and field_.allow_none
        else PYTHON_TO_PROTOBUF_TYPES
    ).get(field_.type_) or field_.type_.__name__


def gen_protobuf_messages(pydantic_base_model: BaseModel):
    """"""

    cls_properties = pydantic_base_model.schema()["properties"]

    def _gen_protobuf_message(field_, enumerate_number: int) -> str:
        proto_fields = extract_proto_fields(cls_properties[field_.name], default_number=enumerate_number)
        if proto_fields["protobuf_message"]:
            return proto_fields["protobuf_message"]
        return "".join(
            f"{tab}{'// disabled: ' if proto_fields.get('disable_rpc', False) else ''}"
            f"{_add_repeated_qualifier(field_.outer_type_)}"
            f"{'u' if proto_fields['is_unsigned'] else ''}{_get_protobuf_type(field_, proto_fields)} "
            f"{field_.name} = {proto_fields['number']};"
        )

    return [
        _gen_protobuf_message(field_, default_number)
        for default_number, field_ in enumerate(pydantic_base_model.__fields__.values(), start=1)
    ]


def pydantic_to_proto(base_model, indent_level: int = 0, prefix_name: str = "") -> str:
    """"""
    pydantic_base_model: BaseModel = base_model

    pydantic_model_meta_class: ModelMetaclass = base_model
    return new_line.join(
        f"{tab * indent_level}{proto_msg_line}"
        for proto_msg_line in [
            f"message {prefix_name}{pydantic_model_meta_class.__qualname__} {{",
            *gen_protobuf_messages(pydantic_base_model),
            f"}}{new_line}",
        ]
    )
