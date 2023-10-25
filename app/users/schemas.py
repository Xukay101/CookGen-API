from pydantic import BaseModel

from app.users.constants import PreferenceType

class UserPreferenceBase(BaseModel):
    preference_type: PreferenceType
    ingredient_id: int

class UserPreferenceCreate(UserPreferenceBase):
    pass

class UserPreferenceRead(UserPreferenceBase):
    id: int

class UserPreferenceUpdate(BaseModel):
    preference_type: PreferenceType | None = None
    ingredient_id: int | None = None

class SavedRecipe(BaseModel):
    recipe_id: int