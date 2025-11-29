import grpc
from proto import auth_pb2

from app.core.db.models.auth import Auth
from app.core.db.repositories.auth_repositories import SQLAlchemyAuthRepository

async def check_reg(
    request,
    context,
)->None:
    
    user_email = await SQLAlchemyAuthRepository().get_user_by_email(request.email,context)
    if user_email is not None:
        await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Email alreaddy registreate")
    
    user_login = await SQLAlchemyAuthRepository().get_user_by_login(request.login,context)
    if user_login is not None:
        await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Username alreaddy registreate")
    
    return None

async def check_in_db(
    db:Auth|None,
    context,
)->None:
    
    if db is None:
        await context.abort(grpc.StatusCode.NOT_FOUND, "Not found")
    return None

async def check_verified_and_in_db(
    db,
    context,
)->None|auth_pb2.Okey:
    
    if db is None:
        await context.abort(grpc.StatusCode.NOT_FOUND, "Not found")
    
    if db.is_verified == False:
        await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "User not comfirm")
    
    return None

async def check_emil_token(
    token_email:list[str]|None,
    context,
)->None:
    if token_email is None:
        await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Token Email")
    return None


async def check_login_token(
    token_email:str|None,
    context,
)->None:
    
    if token_email is None:
        await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Token Username")

    return None

async def check_verify_password(
    result:bool,
    context,
)->None:
    
    if not result:
        await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Password problem")
    
    return None