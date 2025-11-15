from proto import auth_pb2

from app.core.security.token import (
    decode_jwt_email,
    decode_jwt_username,
    create_access_token,
    create_refresh_token,
)
from app.core.security.password import (
    get_password_hash,
    verify_password,
)
from app.core.db.repositories.auth_repositories import SQLAlchemyAuthRepository
from app.gateway.services.iauth_service import IAuthServiceImpl
from app.gateway.utils.cheks import (
    check_reg,
    check_emil_token,
    check_username_token,
)
from app.gateway.utils.convert import (
    convert_create_user,
    
)

class AuthServiceImpl(IAuthServiceImpl):
    def __init__(self):
        self.repo = SQLAlchemyAuthRepository()
    
    async def CreateUser(self, request)->auth_pb2.OkeyResponse:
        response = await check_reg(request)
        if response is not None:
            return response
        hashed_password = get_password_hash(request.password)
        user = convert_create_user(request, hashed_password)
        await self.repo.create_auth_user(user)
        return auth_pb2.OkeyResponse(success=True,status_code = 0, error="")

    async def RegistrationUser(self, request)->auth_pb2.CookieResponse:
        email = decode_jwt_email(request.token_pod)
        response = check_emil_token(email)
        if response is not None:
            return response
        user = await self.repo.get_user_by_email(email)
        if user is None:
            return auth_pb2.CookieResponse(
                access_token="",
                cookie=auth_pb2.Cookie(),
                response=auth_pb2.Okey(success=False, status_code=404, error="User not found")
            )
        access_token = create_access_token({"sub": user.username})
        refresh_token = create_refresh_token({"sub": user.username})
        await self.repo.activate_auth_user(user)
        hash_jwt = get_password_hash(refresh_token)
        await self.repo.add_refresh_token(user,hash_jwt)
        return auth_pb2.CookieResponse(
            access_token=access_token,               
            cookie=auth_pb2.Cookie(
                key = "refresh_token",
                value = refresh_token,
                httponly = False,
                secure = True,
                samesite = "strict",
                max_age = 7*24*3600,
            ),       
            response=auth_pb2.Okey(
                success=True,
                status_code = 0,
                error=""
            )
        )
    async def RefreshToken(self, request)->auth_pb2.AccessTokenResponse:
        username = decode_jwt_username(request.refresh_token)
        response = check_username_token(username)
        if response is not None:
            return response
        user = await self.repo.get_user_by_username(username)
        if user is None:
            return auth_pb2.AccessTokenResponse(
            access_token="",                   
            response=auth_pb2.Okey(
                success=False,
                status_code = 404,
                error="User not found"
                )
            )
        result = verify_password(request.refresh_token,user.refresh_token_hash)
        if not result:
            return auth_pb2.AccessTokenResponse(
            access_token="",                   
            response=auth_pb2.Okey(
                success=False,
                status_code = 400,
                error="Refresh token"
                )
            )
        access_token = create_access_token({"sub": user.username})
        return auth_pb2.AccessTokenResponse(
            access_token=access_token,                   
            response=auth_pb2.Okey(
                success=True,
                status_code = 0,
                error=""
                )
            )

    async def Authenticate(self, request)->auth_pb2.CookieResponse:
        user = await self.repo.get_user_by_username(request.username)
        if user is None:
            return auth_pb2.CookieResponse(
                access_token="",
                cookie=auth_pb2.Cookie(),
                response=auth_pb2.Okey(success=False, status_code=404, error="User not found")
            )
        result = verify_password(request.password,user.password_hash)
        if not result:
            return auth_pb2.CookieResponse(
                access_token="",
                cookie=auth_pb2.Cookie(),
                response=auth_pb2.Okey(success=False, status_code=400, error="Password")
            )
        access_token = create_access_token({"sub": user.username})
        refresh_token = create_refresh_token({"sub": user.username})
        await self.repo.activate_auth_user(user)
        hash_jwt = get_password_hash(refresh_token)
        await self.repo.add_refresh_token(user,hash_jwt)
        return auth_pb2.CookieResponse(
            access_token=access_token,               
            cookie=auth_pb2.Cookie(
                key = "refresh_token",
                value = refresh_token,
                httponly = False,
                secure = True,
                samesite = "strict",
                max_age = 7*24*3600,
            ),       
            response=auth_pb2.Okey(
                success=True,
                status_code = 0,
                error=""
            )
        )
    
    async def CurrentUser(self, request)->auth_pb2.CurrentUserResponse:
        user = await self.repo.get_user_by_username(request.username)
        if user is None:
            return auth_pb2.CurrentUserResponse(
                id = 0,
                username ="",
                is_active = False,
                is_verified = False,
                role ="",
                response=auth_pb2.Okey(success=False, status_code=404, error="User not found")
            )
        if user.is_verified ==False:
            return auth_pb2.CurrentUserResponse(
                id = 0,
                username ="",
                is_active = False,
                is_verified = False,
                role ="",
                response=auth_pb2.Okey(success=False, status_code=400, error="User not comfirm")
            )
        return auth_pb2.CurrentUserResponse(
                id = user.id,
                username = user.username,
                is_active = user.is_active,
                is_verified = user.is_verified,
                role = user.role,
                response=auth_pb2.Okey(success=True, status_code=0, error="")
            )