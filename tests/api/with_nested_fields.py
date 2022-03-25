from fastapi import APIRouter

from tests.models.with_nested_models import WithNestedModelsResponse

router = APIRouter()


@router.get("/with_nested_models", response_model=WithNestedModelsResponse)
async def with_nested_models() -> WithNestedModelsResponse:
    return WithNestedModelsResponse()  # pragma: no cover
