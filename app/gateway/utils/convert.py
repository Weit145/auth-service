from proto import auth_pb2

from app.core.db.models.auth import Auth

def convert_create_user(request,hashed_password)->Auth:
    return Auth(
        username = request.username,
        email = request.email,
        password_hash = hashed_password
    )

def convert_cookie_response(
    access_token:str = "",
    refresh_token:str = "",
    response: auth_pb2.Okey = auth_pb2.Okey(),
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
        response=response,
    )

def convert_access_token_response(
    access_token:str = "",
    response: auth_pb2.Okey = auth_pb2.Okey(),
)->auth_pb2.AccessTokenResponse:
    return auth_pb2.AccessTokenResponse(
            access_token=access_token,                   
            response=response
            )

def convert_current_user_response(
    user:Auth|None = None,
    response: auth_pb2.Okey = auth_pb2.Okey(),
)->auth_pb2.CurrentUserResponse:
    if response is not None:
        return auth_pb2.CurrentUserResponse(
            id = 0,
            username ="",
            is_active = 0,
            is_verified = 0,
            role ="",
            response=response
        )
    return auth_pb2.CurrentUserResponse(
            id = user.id,
            username = user.username,
            is_active = user.is_active,
            is_verified = user.is_verified,
            role = user.role,
            response=auth_pb2.Okey(success=True, status_code=0, error="")
        )

def convert_okey_db(
    result:str,
)->auth_pb2.Okey:
    if result=="":
        return auth_pb2.Okey(
        success=True,
        status_code=0,
        error=result,
        )
    return auth_pb2.Okey(
        success=False,
        status_code=400,
        error=result,
    )