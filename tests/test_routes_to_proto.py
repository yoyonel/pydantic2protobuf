from pydantic2protobuf.services.fastapi_to_proto import gen_proto_file_contents
from tests.api.with_containers import router as router_with_containers
from tests.api.with_nested_fields import router as router_with_nested_models


def test_router_with_nested_models():
    proto = gen_proto_file_contents(router_with_nested_models.routes)
    print(proto)
    assert proto


def test_router_with_containers():
    proto = gen_proto_file_contents(router_with_containers.routes)
    # FIXME: remove this print (debug purpose)
    print(proto)
    assert "rpc do_with_response_list (google.protobuf.Empty) returns (stream WithBasicTypes);" in proto
    assert "rpc do_with_request_list (stream WithBasicTypes)" in proto
