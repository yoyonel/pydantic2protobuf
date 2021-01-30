from dataclasses import dataclass
from typing import Type

from parametrization import Parametrization
from pydantic import BaseModel

from pydantic2protobuf.services.pydantic_to_proto import pydantic_to_proto
from tests.models.with_basic_types import WithBasicTypes
from tests.models.with_nested_models import WithNestedModelsResponse
from tests.models.with_optional_fields import WithOptionalFields
from tests.models.with_repeated_fields import WithRepeatedFields
from tests.tools.parametrization_case import IParametrizationCase


@dataclass
class ParametrizationCase(IParametrizationCase):
    pydantic_model: Type[BaseModel]


@Parametrization.autodetect_parameters()
@IParametrizationCase.case(ParametrizationCase("Pydantic model with basic types", WithBasicTypes))
@IParametrizationCase.case(ParametrizationCase("Pydantic model with optional fields", WithOptionalFields))
@IParametrizationCase.case(ParametrizationCase("Pydantic model with nested models", WithNestedModelsResponse))
@IParametrizationCase.case(ParametrizationCase("Pydantic model with repeated fields", WithRepeatedFields))
def test_pydantic_model_to_proto_msg(pydantic_model):
    generated_proto_msg = pydantic_to_proto(pydantic_model)
    assert generated_proto_msg == pydantic_model.__expected_proto__
