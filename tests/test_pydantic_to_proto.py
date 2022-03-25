from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import pytest
from parametrization import Parametrization  # type: ignore
from pydantic import BaseModel
from pydantic import create_model as create_pydantic_model

from pydantic2protobuf.services.pydantic_to_proto import (
    FieldDefinition,
    ManualProtoMessageDefinition,
    MessageDefinition,
    PydanticFieldDefinition,
    gen_message_definition,
    translate_type,
)
from pydantic2protobuf.tools.from_pydantic import ProtoFieldsDefinition
from tests.models.with_basic_types import WithBasicTypes
from tests.models.with_nested_models import WithNestedModelsResponse
from tests.models.with_optional_fields import WithOptionalFields
from tests.models.with_protobuf_message import WithProtobufMessage
from tests.models.with_repeated_fields import WithRepeatedFields
from tests.tools.parametrization_case import IParametrizationCase


def build_field_definition(**kwargs) -> FieldDefinition:
    if kwargs.get("protobuf_message"):
        return ManualProtoMessageDefinition(proto_message=kwargs["protobuf_message"])  # pragma: no cover
    return PydanticFieldDefinition(
        **{  # type: ignore
            **{
                "disable_rpc": False,
                "is_iterable": False,
                "is_unsigned": False,
            },
            **kwargs,
        }
    )


@pytest.mark.parametrize(
    "base_model,expected_message_definition",
    [
        pytest.param(
            WithBasicTypes,
            MessageDefinition(
                name='WithBasicTypes',
                fields=[
                    build_field_definition(
                        field_name='float_field',
                        type_translated='float',
                        field_number=1,
                    ),
                    build_field_definition(
                        field_name='integer_field',
                        type_translated='int32',
                        field_number=2,
                    ),
                    build_field_definition(
                        field_name='unsigned_integer_field',
                        type_translated='uint32',
                        field_number=3,
                    ),
                ],
            ),
            id="with basic types",
        ),
        pytest.param(
            WithOptionalFields,
            MessageDefinition(
                name='WithOptionalFields',
                fields=[
                    build_field_definition(
                        field_name='optional_string', type_translated='google.protobuf.StringValue', field_number=1
                    ),
                    build_field_definition(
                        field_name='optional_int',
                        type_translated='google.protobuf.UInt32Value',
                        field_number=2,
                    ),
                ],
            ),
            id="with optional fields",
        ),
        pytest.param(
            WithNestedModelsResponse,
            MessageDefinition(
                name='WithNestedModelsResponse',
                fields=[
                    build_field_definition(
                        field_name='webserver',
                        type_translated='WebServerInfos',
                        field_number=1,
                    ),
                    build_field_definition(
                        field_name='grpc',
                        type_translated='GRPCInfo',
                        field_number=2,
                    ),
                    build_field_definition(
                        field_name='app',
                        type_translated='StartupInfos',
                        field_number=3,
                    ),
                ],
            ),
            id="with nested models response",
        ),
        pytest.param(
            WithRepeatedFields,
            MessageDefinition(
                name='WithRepeatedFields',
                fields=[
                    build_field_definition(
                        field_name='repeated_string_field', type_translated='string', is_iterable=True, field_number=1
                    ),
                    build_field_definition(
                        field_number=2,
                        field_name='repeated_structured_type_field',
                        is_iterable=True,
                        type_translated='WithBasicTypes',
                    ),
                ],
            ),
            id="with repeated fields",
        ),
        pytest.param(
            WithProtobufMessage,
            MessageDefinition(
                name='WithProtobufMessage',
                fields=[
                    build_field_definition(field_name='float_field', type_translated='float', field_number=1),
                    build_field_definition(field_number=2, field_name='integer_field', type_translated='int32'),
                    ManualProtoMessageDefinition(
                        proto_message="""\
message WithProtobufMessageField {
    message TupleIds {
        uint32 id_a = 1;
        uint32 id_b = 2;
    }
    repeated TupleIds paired_ids = 1;
}
WithProtobufMessageField pairedIds = 3;"""
                    ),
                ],
            ),
            id="with protobuf message",
        ),
    ],
)
def test_pydantic_model_to_message_definition(base_model, expected_message_definition):
    message_definition = gen_message_definition(base_model)
    assert message_definition == expected_message_definition


@dataclass
class ImpParametrizationCase(IParametrizationCase):
    field_definition: Dict[str, Tuple]
    repeated_qualifier_expected: str


@dataclass
class ImpParametrizationCaseWithDefaults(ImpParametrizationCase):
    proto_fields: ProtoFieldsDefinition = field(
        default_factory=lambda: ProtoFieldsDefinition(
            number=1,
            protobuf_message=None,
            allow_none=False,
            is_unsigned=True,
            disable_rpc=False,
        )
    )


@Parametrization.autodetect_parameters()
@IParametrizationCase.case(
    ImpParametrizationCaseWithDefaults(
        "with repeated string", {"repeated_string_field": (List[str], None)}, repeated_qualifier_expected='string'
    )
)
@IParametrizationCase.case(
    ImpParametrizationCaseWithDefaults(
        "with integer", {"integer_field": (int, None)}, repeated_qualifier_expected='int32'
    )
)
@IParametrizationCase.case(
    ImpParametrizationCaseWithDefaults(
        "with optional string",
        {"optional_string_field": (Optional[str], None)},
        repeated_qualifier_expected='google.protobuf.StringValue',
        proto_fields=ProtoFieldsDefinition(
            number=1,
            protobuf_message=None,
            allow_none=True,
            is_unsigned=False,
            disable_rpc=False,
        ),
    )
)
def test_get_protobuf_type(field_definition, repeated_qualifier_expected, proto_fields):
    pydantic_model = create_pydantic_model("", **field_definition, __base__=BaseModel).__fields__[
        next(iter(field_definition.keys()))
    ]
    assert translate_type(pydantic_model, proto_fields) == repeated_qualifier_expected
