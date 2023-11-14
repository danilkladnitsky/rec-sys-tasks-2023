from typing import List

from fastapi import APIRouter, FastAPI, Request
from pydantic import BaseModel

from service.api.exceptions import UserNotFoundError, ModelNotFoundError
from service.log import app_logger

from service.ml.model_manager import get_model_by_name, Models


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


router = APIRouter()


@router.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    return "I am alive"


@router.get(
    path="/reco/{model_name}/{user_id}",
    tags=["Recommendations"],
    response_model=RecoResponse,
)
async def get_reco(
    request: Request,
    model_name: str,
    user_id: int,
) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    requested_model = get_model_by_name(model_name, user_id)

    if (requested_model == None):
        raise ModelNotFoundError(error_message=f"Requested  model with name '{model_name}' wasn't registered yet")

    return RecoResponse(user_id=user_id, items=requested_model.get_reco(user_id))


def add_views(app: FastAPI) -> None:
    app.include_router(router)
