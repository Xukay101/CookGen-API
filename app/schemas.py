# Global schemas
from datetime import datetime

from pydantic import BaseModel, EmailStr, HttpUrl

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    password: str
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None


# Recipe Schemas
class RecipeBase(BaseModel):
    title: str
    ingredients: str
    instructions: str

class RecipeCreate(RecipeBase):
    pass

class RecipeRead(RecipeBase):
    id: int
    author_id: int
    image_name: str | None = None
    created_at: datetime | None
    updated_at: datetime | None

class RecipeUpdate(BaseModel):
    title: str | None = None
    ingredients: str | None = None
    instructions: str | None = None
    image_name: str | None = None
    author_id: int | None = None

class RecipeImage(BaseModel):
    id: int
    image_url: HttpUrl | None = None