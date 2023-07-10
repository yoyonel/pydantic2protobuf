from dataclasses import dataclass

from parametrization import Parametrization  # type: ignore

from pydantic2protobuf.tools.from_pydantic import ProtoFieldsDefinition, extract_proto_fields, gen_extra_fields
from tests.tools.parametrization_case import IParametrizationCase


def test_gen_proto_field():
    result_processed = gen_extra_fields(number=1)
    result_expected = {
        "extra": {
            "protobuf": {
                "number": 1,
                "protobuf_message": None,
                "allow_none": True,
                "is_unsigned": False,
                "disable_rpc": False,
            }
        }
    }
    assert result_processed == result_expected


@dataclass
class ImpParametrizationCase(IParametrizationCase):
    properties: dict
    proto_fields_expected: ProtoFieldsDefinition

    @staticmethod
    def build_proto_fields_definition(is_unsigned: bool = False) -> ProtoFieldsDefinition:
        return ProtoFieldsDefinition(is_unsigned=is_unsigned)


@Parametrization.autodetect_parameters()
@IParametrizationCase.case(
    ImpParametrizationCase("no extra proto field", {}, ImpParametrizationCase.build_proto_fields_definition())
)
@IParametrizationCase.case(
    ImpParametrizationCase(
        "with dummy properties", {"dummy": "toto"}, ImpParametrizationCase.build_proto_fields_definition()
    )
)
@IParametrizationCase.case(
    ImpParametrizationCase(
        "with an unsigned proto field",
        gen_extra_fields(number=1, is_unsigned=True),
        ImpParametrizationCase.build_proto_fields_definition(is_unsigned=True),
    )
)
def test_extract_proto_fields(properties: dict, proto_fields_expected: ProtoFieldsDefinition):
    proto_fields_computed = extract_proto_fields(properties, default_number=1)
    assert proto_fields_computed == proto_fields_expected
