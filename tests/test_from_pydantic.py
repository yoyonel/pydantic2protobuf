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
class ParametrizationCaseEPF(IParametrizationCase):
    properties: dict
    proto_fields_expected: ProtoFieldsDefinition


def build_proto_fields_definition(is_unsigned: bool = False) -> ProtoFieldsDefinition:
    return ProtoFieldsDefinition(is_unsigned=is_unsigned)


@Parametrization.autodetect_parameters()
@IParametrizationCase.case(ParametrizationCaseEPF("", {}, build_proto_fields_definition()))
@IParametrizationCase.case(ParametrizationCaseEPF("", {"dummy": "toto"}, build_proto_fields_definition()))
@IParametrizationCase.case(
    ParametrizationCaseEPF("", gen_extra_fields(1, is_unsigned=True), build_proto_fields_definition(is_unsigned=True))
)
def test_extract_proto_fields(properties, proto_fields_expected):
    result_processed = extract_proto_fields(properties, default_number=1)
    # FIX: understand why is needed to manually cast into dataclass object here !
    proto_fields_expected = (
        ProtoFieldsDefinition(**proto_fields_expected)
        if isinstance(proto_fields_expected, dict)
        else proto_fields_expected
    )
    assert result_processed == proto_fields_expected
