from dataclasses import dataclass


@dataclass
class PasswordHash:
    value: str

    def verify(self, plain_password: str, verify_function) -> bool:
        return verify_function(plain_password, self.value)
