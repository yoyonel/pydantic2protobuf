import itertools
from typing import Iterator, List, Type

from fastapi.routing import APIRoute
from pydantic.main import ModelMetaclass

from pydantic2protobuf.tools.from_pydantic import extract_model_meta_classes as extract_model_meta_classes_from_mmc


def extract_model_meta_class(route: APIRoute) -> List[Type[ModelMetaclass]]:
    all_model_meta_classes: List[Type[ModelMetaclass]] = []
    # from request field
    if request_field := route.dependant.body_params:
        all_model_meta_classes.extend(extract_model_meta_classes_from_mmc(request_field[0].type_))
    # from response
    if response_field := route.response_field:
        all_model_meta_classes.extend(extract_model_meta_classes_from_mmc(response_field.type_))
    return all_model_meta_classes


def extract_model_meta_classes(routes: Iterator[APIRoute]) -> List[Type[ModelMetaclass]]:
    """"""
    return list(itertools.chain(*(extract_model_meta_class(route) for route in routes)))
