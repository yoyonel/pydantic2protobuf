from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Type

from parametrization import Parametrization
from pydantic import BaseModel
from pydantic import create_model as create_pydantic_model

from pydantic2protobuf.services.pydantic_to_proto import add_repeated_qualifier, gen_message_definition, translate_type
from tests.models import IBaseModelForUTest
from tests.models.with_basic_types import WithBasicTypes
from tests.models.with_nested_models import WithNestedModelsResponse
from tests.models.with_optional_fields import WithOptionalFields
from tests.models.with_repeated_fields import WithRepeatedFields
from tests.tools.parametrization_case import IParametrizationCase


@dataclass
class ParametrizationCasePMTPM(IParametrizationCase):
    pydantic_model: Type[IBaseModelForUTest]


@Parametrization.autodetect_parameters()
@IParametrizationCase.case(ParametrizationCasePMTPM("with basic types", WithBasicTypes))
@IParametrizationCase.case(ParametrizationCasePMTPM("with optional fields", WithOptionalFields))
@IParametrizationCase.case(ParametrizationCasePMTPM("with nested models", WithNestedModelsResponse))
@IParametrizationCase.case(ParametrizationCasePMTPM("with repeated fields", WithRepeatedFields))
def test_pydantic_model_to_proto_msg(pydantic_model: IBaseModelForUTest):
    generated_proto_msg = gen_message_definition(pydantic_model)
    assert generated_proto_msg == pydantic_model._get_expected_protobuf()


@dataclass
class ParametrizationCaseARQ(IParametrizationCase):
    field_definition: Dict[str, Tuple]
    repeated_qualifier_expected: str


@Parametrization.autodetect_parameters()
@IParametrizationCase.case(
    ParametrizationCaseARQ("with optional string", {"text": (Optional[str], None)}, repeated_qualifier_expected='')
)
@IParametrizationCase.case(
    ParametrizationCaseARQ(
        "with strings list", {"texts": (Optional[List[str]], None)}, repeated_qualifier_expected='repeated '
    )
)
def test_add_repeated_qualifier(field_definition, repeated_qualifier_expected):
    pydantic_model = create_pydantic_model("", **field_definition, __base__=BaseModel)
    result_compute = add_repeated_qualifier(pydantic_model.__fields__[list(field_definition.keys())[0]].outer_type_)
    assert result_compute == repeated_qualifier_expected


@dataclass
class ParametrizationCaseGPT(ParametrizationCaseARQ):
    proto_fields: Dict = field(
        default_factory=lambda: {
            'number': 1,
            'protobuf_message': None,
            'allow_none': False,
            'is_unsigned': True,
            'disable_rpc': False,
        }
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
        proto_fields={
            'number': 1,
            'protobuf_message': None,
            'allow_none': True,
            'is_unsigned': False,
            'disable_rpc': False,
        },
    )
)
def test_get_protobuf_type(field_definition, repeated_qualifier_expected, proto_fields):
    pydantic_model = create_pydantic_model("", **field_definition, __base__=BaseModel).__fields__[
        next(iter(field_definition.keys()))
    ]
    assert translate_type(pydantic_model, proto_fields) == repeated_qualifier_expected
