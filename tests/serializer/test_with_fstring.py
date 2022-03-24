from typing import List, Optional

import pytest

from pydantic2protobuf.services.fastapi_to_proto import ProtoFileContent, gen_proto_file_contents
from pydantic2protobuf.services.pydantic_to_proto import FieldDefinition
from pydantic2protobuf.services.serializer.with_fstring import ProtoFileContentSerializerWithFString
from tests.api.with_containers import router as router_with_containers
from tests.api.with_nested_fields import router as router_with_nested_models

service_name = "ServiceTest"


def _build_field(
    type_translated: str,
    field_name: str,
    field_number: int,
    proto_message: Optional[str] = None,
    disable_rpc: bool = False,
    is_iterable: bool = False,
    is_unsigned: bool = False,
) -> FieldDefinition:
    return FieldDefinition(
        proto_message=proto_message,
        disable_rpc=disable_rpc,
        is_iterable=is_iterable,
        is_unsigned=is_unsigned,
        type_translated=type_translated,
        field_name=field_name,
        field_number=field_number,
    )


@pytest.mark.parametrize(
    "input_router,input_service_name,expected_patterns_to_find",
    [
        pytest.param(
            router_with_nested_models,
            "ServiceRouterWithNestedModels",
            (
                """pydantic2protobuf/services/serializer/with_fstring.py.  DO NOT EDIT!
syntax = "proto3";

// https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct
import "google/protobuf/struct.proto";
import "google/protobuf/wrappers.proto";
import "google/protobuf/empty.proto";
""",
                """service ServiceRouterWithNestedModels {
    rpc do_with_nested_models (google.protobuf.Empty) returns (WithNestedModelsResponse);
}""",
                """message WithNestedModelsResponse {
    WebServerInfos webserver = 1;
    GRPCInfo grpc = 2;
    StartupInfos app = 3;
}""",
                """message GRPCInfo {
    string host_and_port = 1;
    int32 maximum_concurrent_rpc = 2;
    int32 max_workers = 3;
    float timeout = 4;
}""",
                """message StartupInfos {
    google.protobuf.StringValue start_datetime = 1;
    GitInfo git_info = 2;
}""",
                """message WebServerInfos {
    google.protobuf.StringValue start_datetime = 1;
    GitInfo git_info = 2;
    string state = 3;
    string details = 4;
}""",
                """message GitInfo {
    string branch_name = 1;
    string committed_datetime = 2;
    string commit_hex_sha = 3;
}""",
            ),
            id="router with nested models",
        ),
        pytest.param(
            router_with_containers,
            "ServiceRouterWithContainers",
            (
                """pydantic2protobuf/services/serializer/with_fstring.py.  DO NOT EDIT!
syntax = "proto3";

// https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct
import "google/protobuf/struct.proto";
import "google/protobuf/wrappers.proto";
import "google/protobuf/empty.proto";
""",
                """service ServiceRouterWithContainers {""",
                """ rpc do_with_response_list (google.protobuf.Empty) returns (stream WithBasicTypes);""",
                """ rpc do_with_request_list (stream WithBasicTypes) returns (google.protobuf.Empty);""",
                """message WithBasicTypes {
    float float_field = 1;
    int32 integer_field = 2;
    uint32 unsigned_integer_field = 3;
}""",
            ),
            id="router with containers",
        ),
    ],
)
def test_serializer(input_router, input_service_name, expected_patterns_to_find: List[str]):
    proto_file_content_computed: ProtoFileContent = gen_proto_file_contents(
        input_router.routes, service_name=input_service_name
    )
    serializer = ProtoFileContentSerializerWithFString()
    generated_proto = serializer(proto_file_content_computed)
    for expected_pattern_to_find in expected_patterns_to_find:
        assert expected_pattern_to_find in generated_proto
