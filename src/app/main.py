from fastapi import FastAPI, status, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import uvicorn
import requests
import json

load_dotenv()

from database.db import Base, engine, get_db
from database.queries import TravelPlan
from database.models import User
from routers import auth, travel_plans
from middleware.auth import is_authenticated

Base.metadata.create_all(bind=engine)

origins = []

app = FastAPI()

app.include_router(auth.router)
app.include_router(travel_plans.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK, tags=["API Check"])
def check():
    return {
        "message": "Hello World!"
    }

@app.get("/api/notify", status_code=status.HTTP_200_OK, tags=["notify"])
async def send_notif(db: Session = Depends(get_db)):
    TravelPlan.send_notif(db)

@app.post("/api/send_message", status_code=status.HTTP_200_OK)
def send_message(msg: str = Body(...), user_id: int = Depends(is_authenticated), db: Session = Depends(get_db)):
    serverToken = 'AAAA-NMsvHo:APA91bE8CtQnGC7jYX1EH__gaWCJWWSi5Xr5vWmjga55ri74A36uLHEALdbE3JSZ6jhQw9VD7QsFKJA7yPvg3SjbkgbX6Yjm_0egr5TBcYSf_KVwmCIkuMp62ZR-oB5xmLSPE2xV-okD'
    user = User.get_user_by_id(user_id, db)
    headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=' + serverToken,
            }

    body = {
        'notification': {
            'title': 'Watch out for the weather today!',
                'body': msg
        },
        'to':user.fcm_token,
        'priority': 'high',
        #   'data': dataPayLoad,
    }
    response = requests.post("https://fcm.googleapis.com/fcm/send", headers = headers, data=json.dumps(body))
    print(response.status_code)

    print(response.json())


if __name__ == '__main__':
    uvicorn.run(app)
