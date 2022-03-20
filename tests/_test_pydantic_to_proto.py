from dataclasses import dataclass
from typing import Optional, Type

from parametrization import Parametrization  # type: ignore
from pydantic import BaseModel
from pydantic import create_model as create_pydantic_model

from pydantic2protobuf.services.pydantic_to_proto import gen_message_definition
from tests.tools.parametrization_case import IParametrizationCase


@dataclass
class ParametrizationCase(IParametrizationCase):
    pydantic_model: Type[BaseModel]
    expected_proto_msg: str


@Parametrization.autodetect_parameters()
@IParametrizationCase.case(
    ParametrizationCase(
        "Pydantic model with basic types",
        create_pydantic_model("Model", a=(float, ...), b=(int, 10), __base__=BaseModel),
        """message Model {
    float a = 1;
    int32 b = 2;
}""",
    )
)
@IParametrizationCase.case(
    ParametrizationCase(
        "Pydantic model with optional fields",
        create_pydantic_model(
            "InfoSentenceRequest", text=(Optional[str], None), skill_id=(Optional[int], None), __base__=BaseModel
        ),
        """message InfoSentenceRequest {
    google.protobuf.StringValue text = 1;
    google.protobuf.UInt32Value skill_id = 2;
}""",
    )
)
def test_pydantic_model_to_proto_msg(pydantic_model, expected_proto_msg):
    generated_proto_msg = gen_message_definition(pydantic_model)
    assert generated_proto_msg == expected_proto_msg
