import importlib.util
import os
from importlib.machinery import ModuleSpec, SourceFileLoader
from pathlib import Path
from typing import List

import pytest

from pydantic2protobuf.services.fastapi_to_proto import gen_proto_file_contents
from tests.api.with_containers import router as router_with_containers
from tests.api.with_nested_fields import router as router_with_nested_models

service_name = "ServiceTest"


@pytest.mark.parametrize(
    "input_router,input_service_name,expected_patterns_to_find",
    [
        pytest.param(
            router_with_nested_models,
            "ServiceRouterWithNestedModels",
            (
                """pydantic2protobuf/pydantic2protobuf/services/fastapi_to_proto.py.  DO NOT EDIT!
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
                """pydantic2protobuf/pydantic2protobuf/services/fastapi_to_proto.py.  DO NOT EDIT!
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
def test_router_with_nested_models(
    input_router, input_service_name, expected_patterns_to_find: List[str], tmpdir, bash
):
    generated_proto = gen_proto_file_contents(input_router.routes, service_name=input_service_name)
    for expected_pattern_to_find in expected_patterns_to_find:
        assert expected_pattern_to_find in generated_proto

    # use the generated protobuf string with grpc-tools.protoc for generated python stub
    fh = tmpdir.join(f"{input_service_name}.proto")
    fh.write(generated_proto)
    filename = os.path.join(fh.dirname, fh.basename)

    bash.run_script_inline(
        [
            'python -m grpc_tools.protoc '
            f'--proto_path={fh.dirname} '
            f'--python_out={fh.dirname} '
            f'--grpc_python_out={fh.dirname} '
            f'--mypy_out=quiet:{fh.dirname} '
            f'{filename}'
        ]
    )

    pb2_path = Path(fh.dirname) / f"{input_service_name}_pb2.py"
    assert pb2_path.exists()
    assert (Path(fh.dirname) / f"{input_service_name}_pb2.pyi").exists()
    assert (Path(fh.dirname) / f"{input_service_name}_pb2_grpc.py").exists()

    # TODO: replace by a "simple" server implementation of protobuf generated below
    spec: ModuleSpec = importlib.util.spec_from_file_location(f"{input_service_name}_pb2", str(pb2_path))
    assert spec
    module = importlib.util.module_from_spec(spec)
    assert module
    loader: SourceFileLoader = spec.loader  # type: ignore
    assert loader
    loader.exec_module(module)
