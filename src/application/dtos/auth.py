from datetime import date

from pydantic import BaseModel, EmailStr, RootModel

from src.auth.application.dtos import TokenResponseDTO


class RegistrationCompositeRequestDTO(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    nick_name: str
    date_of_birth: date


class RegistrationCompositeResponseDTO(RootModel[TokenResponseDTO]):
    pass
