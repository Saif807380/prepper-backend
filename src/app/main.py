from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import uvicorn

load_dotenv()

from database.db import Base, engine, get_db
from database.queries import TravelPlan
from routers import auth, travel_plans

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

if __name__ == '__main__':
    uvicorn.run(app)
