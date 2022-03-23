from dataclasses import dataclass
from typing import Iterator, Protocol, Union

from fastapi.routing import APIRoute

from pydantic2protobuf.services.with_dataclasses.pydantic_to_proto import MessageDefinition, gen_message_definition
from pydantic2protobuf.tools.from_fastapi import extract_model_meta_classes
from pydantic2protobuf.tools.from_pydantic import is_type_iterable


@dataclass(frozen=True)
class EmptyGoogleType:
    ...


@dataclass(frozen=True)
class TypeDefinition:
    is_iterable: bool
    name: str


MethodResponse = Union[EmptyGoogleType, TypeDefinition]
MethodRequest = Union[EmptyGoogleType, TypeDefinition]


@dataclass(frozen=True)
class MethodDefinition:
    route_name: str
    request: MethodRequest
    response: MethodResponse


@dataclass(frozen=True)
class ServiceDefinition:
    name: str
    methods_definitions: list[MethodDefinition]


@dataclass
class Messages:
    messages: list[MessageDefinition]


@dataclass(frozen=True)
class ProtoFileContent:
    service_definition: ServiceDefinition
    messages: list[MessageDefinition]


class ProtoFileContentSerializer(Protocol):
    def __call__(self, proto_file_content: ProtoFileContent) -> str:
        ...


def gen_service_method_request(route: APIRoute) -> MethodRequest:
    result: MethodRequest
    try:
        request_body_params = route.dependant.body_params[0]
        result = TypeDefinition(
            is_iterable=is_type_iterable(request_body_params.outer_type_), name=request_body_params.type_.__name__
        )
    except IndexError:
        result = EmptyGoogleType()
    return result


def gen_service_method_response(route: APIRoute) -> MethodResponse:
    result: MethodResponse
    try:
        response_field = route.response_field
        result = TypeDefinition(
            is_iterable=is_type_iterable(response_field.outer_type_), name=response_field.type_.__name__
        )
    except AttributeError:
        result = EmptyGoogleType()
    return result


def gen_service_method_definition(route: APIRoute) -> MethodDefinition:
    return MethodDefinition(
        route_name=route.name, request=gen_service_method_request(route), response=gen_service_method_response(route)
    )


def gen_service_definition(service_name, routes) -> ServiceDefinition:
    return ServiceDefinition(
        name=service_name, methods_definitions=[gen_service_method_definition(route) for route in routes]
    )


def gen_messages(routes: Iterator[APIRoute]) -> list[MessageDefinition]:
    return [gen_message_definition(model_meta_class) for model_meta_class in set(extract_model_meta_classes(routes))]


def gen_proto_file_contents(
    routes: Iterator[APIRoute],
    service_name: str = "Service",
) -> ProtoFileContent:
    protobuf_file_content = ProtoFileContent(
        service_definition=gen_service_definition(service_name, routes),
        messages=gen_messages(routes),
    )
    return protobuf_file_content
