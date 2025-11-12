from app.core.db.repositories.auth_repositories import SQLAlchemyAuthRepository
from proto import auth_pb2

async def check_reg(
    request,
)->None|auth_pb2.OkeyResponse:
    user_email = await SQLAlchemyAuthRepository().get_user_by_email(request.email)
    if user_email is not None:
        return auth_pb2.OkeyResponse(success=False,status_code = 400, error="Email alreaddy registreate")
    user_username = await SQLAlchemyAuthRepository().get_user_by_username(request.username)
    if user_username is not None:
        return auth_pb2.OkeyResponse(success=False,status_code = 400, error="Username alreaddy registreate")
    return None

def check_emil_token(
    token_email
)->None|auth_pb2.CookieResponse:
    if token_email is None:
        return auth_pb2.CookieResponse(
        access_token="",               
        cookie=auth_pb2.Cookie(),       
        response=auth_pb2.Okey(
            success=False,
            status_code = 400,
            error="Token Email"
        )
    return None
)

def check_username_token(
    token_email
)->None|auth_pb2.AccessTokenResponse:
    if token_email is None:
        return auth_pb2.AccessTokenResponse(
        access_token="",                   
        response=auth_pb2.Okey(
            success=False,
            status_code = 400,
            error="Token Username"
        )
    return None
)