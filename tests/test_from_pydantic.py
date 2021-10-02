from dataclasses import dataclass

from parametrization import Parametrization  # type: ignore

from pydantic2protobuf.tools.from_pydantic import DEFAULT_DICT_FOR_PROTO_FIELDS, extract_proto_fields, gen_extra_fields
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
    default_number: int
    dict_for_proto_fields_expected: dict


@Parametrization.autodetect_parameters()
@IParametrizationCase.case(ParametrizationCaseEPF("", {}, 1, DEFAULT_DICT_FOR_PROTO_FIELDS))
@IParametrizationCase.case(ParametrizationCaseEPF("", {"dummy": "toto"}, 1, DEFAULT_DICT_FOR_PROTO_FIELDS))
@IParametrizationCase.case(
    ParametrizationCaseEPF(
        "", gen_extra_fields(1, is_unsigned=True), 1, {**DEFAULT_DICT_FOR_PROTO_FIELDS, **{"is_unsigned": True}}
    )
)
def test_extract_proto_fields(properties, default_number, dict_for_proto_fields_expected):
    result_processed = extract_proto_fields(properties, default_number)
    assert result_processed == {**dict_for_proto_fields_expected, **{"number": default_number}}
