from app.core.db.models.auth import Auth

def convert_create_user(request,hashed_password)->Auth:
    return Auth(
        username = request.username,
        email = request.email,
        password_hash = hashed_password
    )