from proto import auth_pb2

from app.core.security.token import (
    decode_jwt_email,
    decode_jwt_username,
    create_access_token_user,
    create_refresh_token,
    create_access_token_email,
)
from app.core.security.password import (
    get_password_hash,
    verify_password,
)
from app.core.kafka.repositories.kafka_repositories import  KafkaRepository
from app.core.db.repositories.auth_repositories import SQLAlchemyAuthRepository
from app.gateway.services.iauth_service import IAuthServiceImpl
from app.gateway.utils.cheks import (
    check_reg,
    check_emil_token,
    check_username_token,
    check_in_db,
    check_verify_password,
    check_verified_and_in_db,
)
from app.gateway.utils.convert import (
    convert_create_user,
    convert_cookie_response,
    convert_okey_db,
    convert_access_token_response,
    convert_current_user_response,
)

class AuthServiceImpl(IAuthServiceImpl):
    def __init__(self):
        self.repo = SQLAlchemyAuthRepository()
        self.kf = KafkaRepository()



    async def CreateUser(self, request)->auth_pb2.Okey:
        response = await check_reg(request)
        if response is not None:
            return response
        
        hashed_password = get_password_hash(request.password)
        user = convert_create_user(request, hashed_password)
        result = await self.repo.create_auth_user(user)
        access_token = create_access_token_email({"sub": request.email})
        print(access_token, flush=True)
        await self.kf.send_message(topic="auth",message=access_token)
        return convert_okey_db(result)



    async def RegistrationUser(self, request)->auth_pb2.CookieResponse:

        email = decode_jwt_email(request.token_pod)
        response = check_emil_token(email)
        if response is not None:
            return convert_cookie_response(response=response)
        
        user = await self.repo.get_user_by_email(email)
        response = check_in_db(user)
        if response is not None:
            return convert_cookie_response(response=response)
        
        access_token = create_access_token_user({"sub": user.username})
        refresh_token = create_refresh_token({"sub": user.username})
        hash_jwt = get_password_hash(refresh_token)

        result = await self.repo.activate_user_with_refresh(user,hash_jwt)
        response = convert_okey_db(result)
        return convert_cookie_response(access_token=access_token, refresh_token=refresh_token,response=response)



    async def RefreshToken(self, request)->auth_pb2.AccessTokenResponse:
        username = decode_jwt_username(request.refresh_token)
        response = check_username_token(username)
        if response is not None:
            return convert_access_token_response(response=response)
        
        user = await self.repo.get_user_by_username(username)
        response = check_in_db(user)
        if response is not None:
            return convert_access_token_response(response=response)
        
        result = verify_password(request.refresh_token,user.refresh_token_hash)
        response = check_verify_password(result)
        if response is not None:
            return convert_access_token_response(response=response)
        
        access_token = create_access_token_user({"sub": username})
        return convert_access_token_response(access_token=access_token)



    async def Authenticate(self, request)->auth_pb2.CookieResponse:
        user = await self.repo.get_user_by_username(request.username)
        response = check_in_db(user)
        if response is not None:
            return convert_cookie_response(response=response)
        
        result = verify_password(request.password,user.password_hash)
        response = check_verify_password(result)
        if response is not None:
            return convert_cookie_response(response=response)
        
        access_token = create_access_token_user({"sub": user.username})
        refresh_token = create_refresh_token({"sub": user.username})

        hash_jwt = get_password_hash(refresh_token)
        result = await self.repo.add_refresh_token(user,hash_jwt)
        response = convert_okey_db(result)
        return convert_cookie_response(access_token=access_token, refresh_token=refresh_token,response=response)



    async def CurrentUser(self, request)->auth_pb2.CurrentUserResponse:
        user = await self.repo.get_user_by_username(request.username)
        response = check_verified_and_in_db(user)
        return convert_current_user_response(user,response)