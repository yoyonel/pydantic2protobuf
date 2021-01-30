from pydantic2protobuf.services.fastapi_to_proto import routes_to_proto
from tests.api.with_containers import router as router_with_containers
from tests.api.with_nested_fields import router as router_with_nested_models


def test_router_with_nested_models():
    proto = routes_to_proto(router_with_nested_models.routes)
    print(proto)
    assert proto


def test_router_with_containers():
    proto = routes_to_proto(router_with_containers.routes)
    print(proto)
    assert "rpc do_with_response_list (google.protobuf.Empty) returns (stream WithBasicTypes);" in proto
    assert "rpc do_with_request_list (stream WithBasicTypes)" in proto
