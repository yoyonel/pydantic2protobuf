from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import pytest
from parametrization import Parametrization  # type: ignore
from pydantic import BaseModel
from pydantic import create_model as create_pydantic_model

from pydantic2protobuf.services.pydantic_to_proto import (
    FieldDefinition,
    MessageDefinition,
    gen_message_definition,
    translate_type,
)
from pydantic2protobuf.tools.from_pydantic import ProtoFieldsDefinition
from tests.models.with_basic_types import WithBasicTypes
from tests.tools.parametrization_case import IParametrizationCase

# @pytest.fixture
# def serializer():
#     return ProtoFileContentSerializerWithFString()
#
#
# @dataclass
# class ParametrizationCasePMTPM(IParametrizationCase):
#     pydantic_model: Type[IBaseModelForUTest]
#
#
# @Parametrization.autodetect_parameters()
# @IParametrizationCase.case(ParametrizationCasePMTPM("with basic types", WithBasicTypes))
# @IParametrizationCase.case(ParametrizationCasePMTPM("with optional fields", WithOptionalFields))
# @IParametrizationCase.case(ParametrizationCasePMTPM("with nested models", WithNestedModelsResponse))
# @IParametrizationCase.case(ParametrizationCasePMTPM("with repeated fields", WithRepeatedFields))
# @IParametrizationCase.case(ParametrizationCasePMTPM("with protobuf message", WithProtobufMessage))
# def test_pydantic_model_to_proto_msg(pydantic_model: IBaseModelForUTest):
#     message_definition = gen_message_definition(pydantic_model)
#     # generated_proto_msg = serializer(message_definition)
#     # assert generated_proto_msg == pydantic_model._get_expected_protobuf()


def build_field_definition(**kwargs) -> FieldDefinition:
    return FieldDefinition(
        **{  # type: ignore
            **{
                "disable_rpc": False,
                "is_iterable": False,
                "is_unsigned": False,
                "proto_message": None,
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
        )
    ]
    # TODO: continue utest params
    # pytest.param(WithOptionalFields, ...)
    # pytest.param(WithNestedModelsResponse, ...)
    # pytest.param(WithRepeatedFields, ...)
    # pytest.param(WithProtobufMessage, ...)
)
def test_pydantic_model_to_message_definition(base_model, expected_message_definition):
    message_definition = gen_message_definition(base_model)
    assert message_definition == expected_message_definition


@dataclass
class ParametrizationCaseARQ(IParametrizationCase):
    field_definition: Dict[str, Tuple]
    repeated_qualifier_expected: str


# @Parametrization.autodetect_parameters()
# @IParametrizationCase.case(
#     ParametrizationCaseARQ("with optional string", {"text": (Optional[str], None)}, repeated_qualifier_expected='')
# )
# @IParametrizationCase.case(
#     ParametrizationCaseARQ(
#         "with strings list", {"texts": (Optional[List[str]], None)}, repeated_qualifier_expected='repeated '
#     )
# )
# def test_add_repeated_qualifier(field_definition, repeated_qualifier_expected):
#     pydantic_model = create_pydantic_model("", **field_definition, __base__=BaseModel)
#     result_compute = add_repeated_qualifier(pydantic_model.__fields__[list(field_definition.keys())[0]].outer_type_)
#     assert result_compute == repeated_qualifier_expected


@dataclass
class ParametrizationCaseGPT(ParametrizationCaseARQ):
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
    ParametrizationCaseGPT(
        "with repeated string", {"repeated_string_field": (List[str], None)}, repeated_qualifier_expected='string'
    )
)
@IParametrizationCase.case(
    ParametrizationCaseGPT("with integer", {"integer_field": (int, None)}, repeated_qualifier_expected='int32')
)
@IParametrizationCase.case(
    ParametrizationCaseGPT(
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
    # FIX: understand why is needed to manually cast into dataclass object here !
    proto_fields = ProtoFieldsDefinition(**proto_fields) if isinstance(proto_fields, dict) else proto_fields
    assert translate_type(pydantic_model, proto_fields) == repeated_qualifier_expected
