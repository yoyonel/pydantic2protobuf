from fastapi import APIRouter

from tests.models.with_repeated_fields import WithRepeatedFields

router = APIRouter()


@router.get("/with_repeated_fields", response_model=WithRepeatedFields)
async def with_repeated_fields(request: WithRepeatedFields):
    assert request  # pragma: no cover
