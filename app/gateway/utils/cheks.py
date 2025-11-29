import grpc
from proto import auth_pb2

from app.core.db.models.auth import Auth
from app.core.db.repositories.auth_repositories import SQLAlchemyAuthRepository

async def check_reg(
    request,
    context,
)->None:
    
    user_email = await SQLAlchemyAuthRepository().get_user_by_email(request.email)
    if user_email is not None:
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Email alreaddy registreate")
    
    user_login = await SQLAlchemyAuthRepository().get_user_by_login(request.login)
    if user_login is not None:
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Username alreaddy registreate")
    
    return None

def check_in_db(
    db:Auth|None,
    context,
)->None:
    
    if db is None:
        context.abort(grpc.StatusCode.NOT_FOUND, "Not found")
    return None

def check_verified_and_in_db(
    db,
    context,
)->None|auth_pb2.Okey:
    
    if db is None:
        context.abort(grpc.StatusCode.NOT_FOUND, "Not found")
    
    if db.is_verified == False:
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, "User not comfirm")
    
    return None

def check_emil_token(
    token_email:list[str]|None,
    context,
)->None:
    if token_email is None:
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Token Email")
    return None


def check_login_token(
    token_email:str|None,
    context,
)->None:
    
    if token_email is None:
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Token Username")

    return None

def check_verify_password(
    result:bool,
    context,
)->None:
    
    if not result:
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Password problem")
    
    return None