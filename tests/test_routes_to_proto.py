from dataclasses import asdict
from typing import Optional

import pytest

from pydantic2protobuf.services.fastapi_to_proto import (
    EmptyGoogleType,
    MethodDefinition,
    ProtoFileContent,
    ServiceDefinition,
    TypeDefinition,
    gen_proto_file_contents,
)
from pydantic2protobuf.services.pydantic_to_proto import FieldDefinition, MessageDefinition
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
    "input_router,input_service_name,proto_file_content_expected",
    [
        pytest.param(
            router_with_nested_models,
            "ServiceRouterWithNestedModels",
            ProtoFileContent(
                service_definition=ServiceDefinition(
                    name='ServiceRouterWithNestedModels',
                    methods_definitions=[
                        MethodDefinition(
                            route_name='with_nested_models',
                            request=EmptyGoogleType(),
                            response=TypeDefinition(is_iterable=False, name='WithNestedModelsResponse'),
                        )
                    ],
                ),
                messages=[
                    MessageDefinition(
                        name='WithNestedModelsResponse',
                        fields=[
                            _build_field('WebServerInfos', 'webserver', field_number=1),
                            _build_field('GRPCInfo', 'grpc', field_number=2),
                            _build_field('StartupInfos', 'app', field_number=3),
                        ],
                    ),
                    MessageDefinition(
                        name='GitInfo',
                        fields=[
                            _build_field('string', 'branch_name', field_number=1),
                            _build_field('string', 'committed_datetime', field_number=2),
                            _build_field('string', 'commit_hex_sha', field_number=3),
                        ],
                    ),
                    MessageDefinition(
                        name='GRPCInfo',
                        fields=[
                            _build_field('string', 'host_and_port', field_number=1),
                            _build_field('int32', 'maximum_concurrent_rpc', field_number=2),
                            _build_field('int32', 'max_workers', field_number=3),
                            _build_field('float', 'timeout', field_number=4),
                        ],
                    ),
                    MessageDefinition(
                        name='WebServerInfos',
                        fields=[
                            _build_field('google.protobuf.StringValue', 'start_datetime', field_number=1),
                            _build_field('GitInfo', 'git_info', field_number=2),
                            _build_field('string', 'state', field_number=3),
                            _build_field('string', 'details', field_number=4),
                        ],
                    ),
                    MessageDefinition(
                        name='StartupInfos',
                        fields=[
                            _build_field('google.protobuf.StringValue', 'start_datetime', field_number=1),
                            _build_field('GitInfo', 'git_info', field_number=2),
                        ],
                    ),
                ],
            ),
            id="router with nested models",
        ),
        pytest.param(
            router_with_containers,
            "ServiceRouterWithContainers",
            ProtoFileContent(
                service_definition=ServiceDefinition(
                    name='ServiceRouterWithContainers',
                    methods_definitions=[
                        MethodDefinition(
                            route_name='with_response_list',
                            request=EmptyGoogleType(),
                            response=TypeDefinition(is_iterable=True, name='WithBasicTypes'),
                        ),
                        MethodDefinition(
                            route_name='with_request_list',
                            request=TypeDefinition(is_iterable=True, name='WithBasicTypes'),
                            response=EmptyGoogleType(),
                        ),
                    ],
                ),
                messages=[
                    MessageDefinition(
                        name='WithBasicTypes',
                        fields=[
                            _build_field('float', 'float_field', field_number=1),
                            _build_field('int32', 'integer_field', field_number=2),
                            _build_field('uint32', 'unsigned_integer_field', field_number=3),
                        ],
                    )
                ],
            ),
            id="router with containers",
        ),
    ],
)
def test_router_with_nested_models(input_router, input_service_name, proto_file_content_expected: ProtoFileContent):
    proto_file_content_computed: ProtoFileContent = gen_proto_file_contents(
        input_router.routes, service_name=input_service_name
    )
    assert proto_file_content_computed.service_definition == proto_file_content_expected.service_definition
    assert sorted(map(asdict, proto_file_content_computed.messages), key=lambda message: message["name"]) == sorted(
        map(asdict, proto_file_content_expected.messages), key=lambda message: message["name"]
    )
