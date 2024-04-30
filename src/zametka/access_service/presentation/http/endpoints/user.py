from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response

from zametka.access_service.application.authorize import Authorize
from zametka.access_service.application.create_user import CreateUser
from zametka.access_service.application.get_user import GetUser
from zametka.access_service.application.verify_email import VerifyEmail

from zametka.access_service.application.dto import UserDTO
from zametka.access_service.application.authorize import AuthorizeInputDTO
from zametka.access_service.application.create_user import CreateUserInputDTO
from zametka.access_service.infrastructure.jwt.access_token_processor import (
    AccessTokenProcessor,
)
from zametka.access_service.infrastructure.jwt.confirmation_token_processor import (
    ConfirmationTokenProcessor,
)
from zametka.access_service.infrastructure.jwt.jwt_processor import JWTToken
from zametka.access_service.presentation.http.jwt.token_auth import TokenAuth

from zametka.access_service.presentation.http.schemas.user import (
    AuthorizeSchema,
    CreateIdentitySchema,
)

router = APIRouter(
    prefix="/access",
    tags=["access"],
    responses={404: {"description": "Не найдено"}},
    route_class=DishkaRoute,
)


@router.post("/")
async def create_identity(
    data: CreateIdentitySchema,
    action: FromDishka[CreateUser],
) -> UserDTO:
    response = await action(
        CreateUserInputDTO(
            email=data.email,
            password=data.password,
        )
    )

    return response


@router.post("/authorize")
async def authorize(
    data: AuthorizeSchema,
    action: FromDishka[Authorize],
    token_processor: FromDishka[AccessTokenProcessor],
    token_auth: FromDishka[TokenAuth],
) -> Response:
    access_token = await action(
        AuthorizeInputDTO(
            email=data.email,
            password=data.password,
        )
    )

    jwt_token = token_processor.encode(access_token)

    http_response = JSONResponse(
        content={
            "token": jwt_token,
        },
    )

    return token_auth.set_access_cookie(jwt_token, http_response)


@router.get("/me")
async def get_identity(action: FromDishka[GetUser]) -> UserDTO:
    response = await action()
    return response


@router.get("/verify/{token}")
async def verify_email(
    token: JWTToken,
    action: FromDishka[VerifyEmail],
    token_processor: FromDishka[ConfirmationTokenProcessor],
) -> None:
    token = token_processor.decode(token)
    await action(token)
