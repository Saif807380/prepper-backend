from fastapi import APIRouter, status, Body, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database import schemas
from database.queries import User, TravelPlan
from middleware.auth import is_autheticated

router = APIRouter(
    prefix="/api/travel_plans",
    tags=["travel_plans"]
)

@router.get('/', status_code=status.HTTP_200_OK)
def get_plans(user_id: int = Depends(is_autheticated), db: Session = Depends(get_db)):
    user = User.get_user_by_id(user_id, db)
    return { "plans": user.plans }

@router.post('/', status_code=status.HTTP_200_OK)
def create_plan(plan: schemas.TravelPlanBase, user_id: int = Depends(is_autheticated), db: Session = Depends(get_db)):
    user = User.get_user_by_id(user_id, db)
    db_plan = TravelPlan.create_plan(user, plan, db)
    return { "plan": db_plan }
