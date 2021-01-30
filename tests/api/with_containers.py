from typing import List

from fastapi import APIRouter

from tests.models.with_basic_types import WithBasicTypes

router = APIRouter()


@router.get("/with_response_list", response_model=List[WithBasicTypes])
async def with_response_list() -> List[WithBasicTypes]:
    return []


@router.get("/with_request_list")
async def with_request_list(requests: List[WithBasicTypes]):
    assert requests
