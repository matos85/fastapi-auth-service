from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="secret")


class UserUpdate(BaseModel):
    email: EmailStr | None = Field(None, example="new@example.com")
    password: str | None = Field(None, min_length=6, example="newsecret")


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com"
            }
        }