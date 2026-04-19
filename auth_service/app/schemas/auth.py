from pydantic import BaseModel, EmailStr, field_validator
import re

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        # Регулярное выражение для формата student_surname@email.com
        # Допускаем любое имя пользователя, но домен должен быть @email.com (или @email)
        if not re.match(r"^[a-zA-Z0-9._%+-]+@email(\.com)?$", v):
            raise ValueError("Email must be in format 'student_surname@email.com'")
        return v

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
