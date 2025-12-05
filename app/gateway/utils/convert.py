from proto import auth_pb2

from app.core.db.models.auth import Auth

default = auth_pb2.Okey(
    success=True,
    )

def convert_create_user(request,hashed_password)->Auth:
    return Auth(
        login = request.login,
        email = request.email,
        password_hash = hashed_password
    )

def convert_cookie_response(
    access_token:str = "",
    refresh_token:str = "",
)->auth_pb2.CookieResponse:
    
    cookie=auth_pb2.Cookie(
                key = "refresh_token",
                value = refresh_token,
                httponly = False,
                secure = True,
                samesite = "strict",
                max_age = 7*24*3600,
            )
    
    return auth_pb2.CookieResponse(
        access_token=access_token,               
        cookie=cookie,       
    )

def convert_access_token_response(
    access_token:str = "",
)->auth_pb2.AccessTokenResponse:
    return auth_pb2.AccessTokenResponse(
            access_token=access_token,                   
            )

def convert_current_user_response(
    user:Auth|None = None,
)->auth_pb2.CurrentUserResponse:
    return auth_pb2.CurrentUserResponse(
            id = user.id,
            login = user.login,
            is_active = user.is_active,
            is_verified = user.is_verified,
            role = user.role,
        )
