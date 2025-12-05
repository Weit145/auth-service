from app.core.config import settings

class PasswordService:
    
    @staticmethod
    def get_password_hash(password) -> str:
        return settings.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return settings.pwd_context.verify(plain_password, hashed_password)