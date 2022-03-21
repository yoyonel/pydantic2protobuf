from dataclasses import asdict

import pytest

from pydantic2protobuf.services.j2_fastapi_to_proto import (
    MethodDefinition,
    MethodRequest,
    ProtoFileContent,
    ServiceDefinition,
    gen_proto_file_contents,
)
from pydantic2protobuf.services.j2_pydantic_to_proto import FieldDefinition, MessageDefinition
from tests.api.with_nested_fields import router as router_with_nested_models

service_name = "ServiceTest"


@pytest.mark.parametrize(
    "input_router,input_service_name,expected_result",
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
                            request=MethodRequest(empty_google_type=True, is_type_iterable=False, type_name=None),
                            response=MethodRequest(
                                empty_google_type=False, is_type_iterable=False, type_name='WithNestedModelsResponse'
                            ),
                        )
                    ],
                ),
                messages=[
                    MessageDefinition(
                        name='WithNestedModelsResponse',
                        fields=[
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='WebServerInfos',
                                field_name='webserver',
                                field_number=1,
                            ),
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='GRPCInfo',
                                field_name='grpc',
                                field_number=2,
                            ),
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='StartupInfos',
                                field_name='app',
                                field_number=3,
                            ),
                        ],
                    ),
                    MessageDefinition(
                        name='GitInfo',
                        fields=[
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='string',
                                field_name='branch_name',
                                field_number=1,
                            ),
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='string',
                                field_name='committed_datetime',
                                field_number=2,
                            ),
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='string',
                                field_name='commit_hex_sha',
                                field_number=3,
                            ),
                        ],
                    ),
                    MessageDefinition(
                        name='GRPCInfo',
                        fields=[
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='string',
                                field_name='host_and_port',
                                field_number=1,
                            ),
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='int32',
                                field_name='maximum_concurrent_rpc',
                                field_number=2,
                            ),
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='int32',
                                field_name='max_workers',
                                field_number=3,
                            ),
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='float',
                                field_name='timeout',
                                field_number=4,
                            ),
                        ],
                    ),
                    MessageDefinition(
                        name='WebServerInfos',
                        fields=[
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='google.protobuf.StringValue',
                                field_name='start_datetime',
                                field_number=1,
                            ),
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='GitInfo',
                                field_name='git_info',
                                field_number=2,
                            ),
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='string',
                                field_name='state',
                                field_number=3,
                            ),
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='string',
                                field_name='details',
                                field_number=4,
                            ),
                        ],
                    ),
                    MessageDefinition(
                        name='StartupInfos',
                        fields=[
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='google.protobuf.StringValue',
                                field_name='start_datetime',
                                field_number=1,
                            ),
                            FieldDefinition(
                                proto_message=None,
                                disable_rpc=False,
                                is_iterable=False,
                                is_unsigned=False,
                                type_translated='GitInfo',
                                field_name='git_info',
                                field_number=2,
                            ),
                        ],
                    ),
                ],
            ),
            id="router with nested models",
        ),
        # pytest.param(
        #     router_with_containers,
        #     "ServiceRouterWithContainers",
        #     {},
        #     id="router with containers",
        # ),
    ],
)
def test_j2_router_with_nested_models(
    input_router, input_service_name, expected_result: ProtoFileContent, tmpdir, bash
):
    json_proto_computed = gen_proto_file_contents(input_router.routes, service_name=input_service_name)
    assert json_proto_computed.service_definition == expected_result.service_definition
    assert sorted(map(asdict, json_proto_computed.messages), key=lambda message: message["name"]) == sorted(
        map(asdict, expected_result.messages), key=lambda message: message["name"]
    )
