from proto import auth_pb2
from app.core.security.token import (
    decode_jwt_email,
    decode_jwt_login,
    create_access_token_user,
    create_refresh_token,
    create_access_token_email,
)
from app.core.security.password import (
    get_password_hash,
    verify_password,
)
from app.kafka.repositories.kafka_repositories import KafkaRepository
from app.core.db.repositories.auth_repositories import SQLAlchemyAuthRepository
from app.gateway.services.iauth_service import IAuthServiceImpl
from app.gateway.utils.cheks import (
    check_reg,
    check_emil_token,
    check_login_token,
    check_in_db,
    check_verify_password,
    check_verified_and_in_db,
)
from app.gateway.utils.convert import (
    convert_create_user,
    convert_cookie_response,
    convert_access_token_response,
    convert_current_user_response,
)


class AuthServiceImpl(IAuthServiceImpl):
    def __init__(self):
        self.repo = SQLAlchemyAuthRepository()
        self.kf = KafkaRepository()

    async def CreateUser(self, request, context) -> auth_pb2.Okey:
        await check_reg(request, context)

        hashed_password = get_password_hash(request.password)
        user = convert_create_user(request, hashed_password)
        await self.repo.create_auth_user(user, context)
        user_bd = await self.repo.get_user_by_email(user.email, context)
        await check_in_db(user, context)

        access_token = create_access_token_email(
            {"sub": request.email, "username": request.username}
        )
        print(access_token, flush=True)
        await self.kf.send_message(
            topic="auth",
            message={
                "id":user_bd.id,
                "token": access_token,
                "username": request.username,
                "email": request.email,
            },
        )

        return auth_pb2.Okey(success=True)

    async def RegistrationUser(self, request, context) -> auth_pb2.CookieResponse:
        decode = decode_jwt_email(request.token_pod)
        await check_emil_token(decode, context)

        user = await self.repo.get_user_by_email(decode[0], context)
        await check_in_db(user, context)

        access_token = create_access_token_user({"sub": user.login})
        refresh_token = create_refresh_token({"sub": user.login})
        hash_jwt = get_password_hash(refresh_token)

        await self.repo.activate_user_with_refresh(user, hash_jwt, context)

        await self.kf.send_message(
            topic="registration",
            message={
                "id": user.id,
                "username": decode[1],
            },
        )

        return convert_cookie_response(
            access_token=access_token, refresh_token=refresh_token
        )

    async def RefreshToken(self, request, context) -> auth_pb2.AccessTokenResponse:
        login = decode_jwt_login(request.refresh_token)
        await check_login_token(login, context)

        user = await self.repo.get_user_by_login(login, context)
        await check_in_db(user, context)

        result = verify_password(request.refresh_token, user.refresh_token_hash)
        await check_verify_password(result, context)

        access_token = create_access_token_user({"sub": login})
        return convert_access_token_response(access_token=access_token)

    async def Authenticate(self, request, context) -> auth_pb2.CookieResponse:
        user = await self.repo.get_user_by_login(request.login, context)
        await check_in_db(user, context)

        result = verify_password(request.password, user.password_hash)
        await check_verify_password(result, context)

        access_token = create_access_token_user({"sub": user.login})
        refresh_token = create_refresh_token({"sub": user.login})

        hash_jwt = get_password_hash(refresh_token)
        result = await self.repo.add_refresh_token(user, hash_jwt, context)
        return convert_cookie_response(
            access_token=access_token, refresh_token=refresh_token
        )

    async def CurrentUser(self, request, context) -> auth_pb2.CurrentUserResponse:
        login = decode_jwt_login(request.access_token)
        await check_login_token(login, context)

        user = await self.repo.get_user_by_login(login, context)
        await check_verified_and_in_db(user, context)
        return convert_current_user_response(user)

    async def LogOutUser(self, request, context) -> auth_pb2.Empty:
        login = decode_jwt_login(request.token_pod)
        await check_login_token(login, context)

        user = await self.repo.get_user_by_login(login, context)
        await check_verified_and_in_db(user, context)

        await self.repo.delete_refresh(user)
        return auth_pb2.Empty()

    async def DeleteUserFromUserService(self, data: dict) -> None:
        id = data.get("id")
        print(f"Deleting auth user with ID: {id}", flush=True)
        user = await self.repo.get_user_by_id(id)
        if user is not None:
            await self.repo.delete_auth_user(user)


    async def DeleteNoVerifiedUser(self, data: dict)->None:
        id = data.get("id")
        user = await self.repo.get_user_by_id(id)
        if not user.is_verified:
            await self.repo.delete_auth_user(user)