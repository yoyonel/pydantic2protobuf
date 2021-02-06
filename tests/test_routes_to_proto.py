from pydantic2protobuf.services.fastapi_to_proto import gen_proto_file_contents
from tests.api.with_containers import router as router_with_containers
from tests.api.with_nested_fields import router as router_with_nested_models


def test_router_with_nested_models():
    patterns_to_find = (
        """// Generated by /home/latty/Prog/__PYTHON__/pydantic2protobuf/pydantic2protobuf/services/fastapi_to_proto.py.  DO NOT EDIT!
syntax = "proto3";

// https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct
import "google/protobuf/struct.proto";
import "google/protobuf/wrappers.proto";
import "google/protobuf/empty.proto";
""",
        """service Service {
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
    )
    proto = gen_proto_file_contents(router_with_nested_models.routes)
    for pattern_to_find in patterns_to_find:
        assert pattern_to_find in proto


def test_router_with_containers():
    proto = gen_proto_file_contents(router_with_containers.routes)
    patterns_to_find = (
        """// Generated by /home/latty/Prog/__PYTHON__/pydantic2protobuf/pydantic2protobuf/services/fastapi_to_proto.py.  DO NOT EDIT!
syntax = "proto3";

// https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct
import "google/protobuf/struct.proto";
import "google/protobuf/wrappers.proto";
import "google/protobuf/empty.proto";
""",
        """service Service {""",
        """ rpc do_with_response_list (google.protobuf.Empty) returns (stream WithBasicTypes);""",
        """ rpc do_with_request_list (stream WithBasicTypes) returns (google.protobuf.Empty);""",
        """message WithBasicTypes {
    float float_field = 1;
    int32 integer_field = 2;
    uint32 unsigned_integer_field = 3;
}""",
    )
    for pattern_to_find in patterns_to_find:
        assert pattern_to_find in proto
