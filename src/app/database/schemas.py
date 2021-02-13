from pydantic import BaseModel
from datetime import date

class Token(BaseModel):
    access_token: str

# Base class is schema for request body
class UserBase(BaseModel):
    email: str
    full_name: str
    password: str
    fcm_token: str

# Schema class is schema for response body and db object
class UserSchema(UserBase):
    id: int
    plans: list
    # allows conversion between Pydantic and ORMs
    class Config:
        orm_mode = True

class TravelPlanBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    cities: list = []
    pills: list = []

class TravelPlanSchema(TravelPlanBase):
    id: int
    user_id: int