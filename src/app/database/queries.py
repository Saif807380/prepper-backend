from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import requests
import json

from . import models, schemas
from helpers.auth import get_password_hash
from exceptions.user import user_already_exists_exception
from exceptions.plan import plan_already_exists_exception

class User:

    @staticmethod
    def get_user_by_id(id: int, db: Session):
        return db.query(models.User).filter(models.User.id == id).first()

    @staticmethod
    def get_user_by_email(email: str, db: Session):
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def create_user(user: schemas.UserBase, db: Session):
        try:
            user.password = get_password_hash(user.password)
            db_user = models.User(**user.dict())
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            raise user_already_exists_exception


class TravelPlan:

    @staticmethod
    def create_plan(user: schemas.UserSchema, plan: schemas.TravelPlanBase, db: Session):
        try:
            db_plan = models.TravelPlan(name=plan.name, start_date=plan.start_date, end_date=plan.end_date, user_id=user.id)
            db_plan.cities = [models.City(name=city) for city in plan.cities]
            db_plan.pills = [models.Pill(name=pill["name"], dosage=pill["dosage"], stock=pill["stock"], time=pill["time"], period=pill["period"]) for pill in plan.pills]
            db.add(db_plan)
            db.commit()
            db.refresh(db_plan)
            return db_plan
        except IntegrityError:
            raise plan_already_exists_exception

    @staticmethod
    def send_notif(db: Session):
        db_pills = db.query(models.Pill).all()
        users = []
        for pill in db_pills:
            p = None
            if pill.period == 'daily':
                p = 1
            elif pill.period == 'weekly':
                p = 7
            if pill.time == datetime.now().time() and pill.stock > 0 and (pill.last_sent==None or datetime.now() - pill.last_sent >= timedelta(minutes=p)):
                users.extend([plan.user_id for plan in pill.plans])
                if pill.last_sent:
                    pill.last_sent += timedelta(minutes=p)
                else:
                    pill.last_sent = datetime.now()
        print(users)
        for id in users:
            user = db.query(models.User).filter(models.User.id == id).first()
            serverToken = 'AAAA-NMsvHo:APA91bE8CtQnGC7jYX1EH__gaWCJWWSi5Xr5vWmjga55ri74A36uLHEALdbE3JSZ6jhQw9VD7QsFKJA7yPvg3SjbkgbX6Yjm_0egr5TBcYSf_KVwmCIkuMp62ZR-oB5xmLSPE2xV-okD'
            deviceToken = user.fcm_token
            print(deviceToken)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=' + serverToken,
            }

            body = {
                'notification': {
                    'title': 'Reminder!',
                        'body': "It's time to take your pills"
                },
                'to':deviceToken,
                'priority': 'high',
                #   'data': dataPayLoad,
            }
            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
            print(response.status_code)

            print(response.json())