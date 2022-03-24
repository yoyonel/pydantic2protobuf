from dataclasses import asdict, dataclass
from typing import Optional, Type

from parametrization import Parametrization  # type: ignore
from pydantic import BaseModel
from pydantic import create_model as create_pydantic_model

from pydantic2protobuf.services.pydantic_to_proto import FieldDefinition, MessageDefinition, gen_message_definition
from tests.tools.parametrization_case import IParametrizationCase


@dataclass
class ParametrizationCase(IParametrizationCase):
    pydantic_model: Type[BaseModel]
    expected_msg_definition: dict


@Parametrization.autodetect_parameters()
@IParametrizationCase.case(
    ParametrizationCase(
        "Pydantic model with basic types",
        create_pydantic_model("Model", a=(float, ...), b=(int, 10), __base__=BaseModel),
        asdict(
            MessageDefinition(
                name='Model',
                fields=[
                    FieldDefinition(
                        field_name='a',
                        type_translated='float',
                        disable_rpc=False,
                        is_iterable=False,
                        is_unsigned=False,
                        field_number=1,
                        proto_message=None,
                    ),
                    FieldDefinition(
                        field_name='b',
                        type_translated='int32',
                        disable_rpc=False,
                        is_iterable=False,
                        is_unsigned=False,
                        field_number=2,
                        proto_message=None,
                    ),
                ],
            )
        ),
    )
)
@IParametrizationCase.case(
    ParametrizationCase(
        "Pydantic model with optional fields",
        create_pydantic_model(
            "InfoSentenceRequest", text=(Optional[str], None), skill_id=(Optional[int], None), __base__=BaseModel
        ),
        asdict(
            MessageDefinition(
                name='InfoSentenceRequest',
                fields=[
                    FieldDefinition(
                        field_name='text',
                        type_translated='google.protobuf.StringValue',
                        disable_rpc=False,
                        is_iterable=False,
                        is_unsigned=False,
                        field_number=1,
                        proto_message=None,
                    ),
                    FieldDefinition(
                        field_name='skill_id',
                        type_translated='google.protobuf.Int64Value',
                        disable_rpc=False,
                        is_iterable=False,
                        is_unsigned=False,
                        field_number=2,
                        proto_message=None,
                    ),
                ],
            )
        ),
    )
)
def test_gen_message_definition(pydantic_model, expected_msg_definition):
    generated_msg_definition = gen_message_definition(pydantic_model)
    assert asdict(generated_msg_definition) == expected_msg_definition
