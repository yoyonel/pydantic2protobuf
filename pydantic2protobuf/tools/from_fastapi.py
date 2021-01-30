from typing import List, Type

from fastapi.routing import APIRoute
from pydantic.main import ModelMetaclass

from pydantic2protobuf.tools.from_pydantic import extract_model_meta_classes as extract_model_meta_classes_from_mmc


def extract_model_meta_classes(routes: List[APIRoute]) -> List[Type[ModelMetaclass]]:
    """

    :param routes:
    :return:
    """
    all_model_meta_classes: List[Type[ModelMetaclass]] = []
    for route in routes:
        # from request field
        request_body_params = route.dependant.body_params
        if request_body_params:
            request_field = request_body_params[0]
            if request_field is not None and isinstance(request_field.type_, ModelMetaclass):
                all_model_meta_classes.extend(extract_model_meta_classes_from_mmc(request_field.type_))
        # from response field
        response_field = route.response_field
        if response_field is not None and isinstance(response_field.type_, ModelMetaclass):
            all_model_meta_classes.extend(extract_model_meta_classes_from_mmc(response_field.type_))
    return all_model_meta_classes
