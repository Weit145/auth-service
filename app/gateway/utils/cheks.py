from proto import auth_pb2

from app.core.db.models.auth import Auth
from app.core.db.repositories.auth_repositories import SQLAlchemyAuthRepository

async def check_reg(
    request,
)->None|auth_pb2.Okey:
    user_email = await SQLAlchemyAuthRepository().get_user_by_email(request.email)
    if user_email is not None:
        return auth_pb2.Okey(success=False,status_code = 400, error="Email alreaddy registreate")
    user_username = await SQLAlchemyAuthRepository().get_user_by_username(request.username)
    if user_username is not None:
        return auth_pb2.Okey(success=False,status_code = 400, error="Username alreaddy registreate")
    return None

async def check_in_db(
    db:Auth|None,
)->None|auth_pb2.Okey:
    if db is None:
        return auth_pb2.Okey(success=False,status_code = 404, error="Not found")
    return None

def check_verified_and_in_db(
    db,
)->None|auth_pb2.Okey:
    if db is None:
        return auth_pb2.Okey(success=False,status_code = 404, error="Not found")
    if db.is_verified == False:
        return auth_pb2.Okey(success=False, status_code=400, error="User not comfirm")
    return None

def check_emil_token(
    token_email:str|None,
)->None|auth_pb2.Okey:
    if token_email is None:
        return auth_pb2.Okey(
            success=False,
            status_code = 400,
            error="Token Email"
        )
    return None


def check_username_token(
    token_email:str|None,
)->None|auth_pb2.Okey:
    if token_email is None:
        return auth_pb2.Okey(
            success=False,
            status_code = 400,
            error="Token Username"
        )
    return None

def check_verify_password(
    result:bool,
)->None|auth_pb2.Okey:
    if not result:
        return auth_pb2.Okey(
                success=False,
                status_code = 400,
                error="Refresh token"
            )
    return None