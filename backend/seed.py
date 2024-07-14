from sqlalchemy import select
from sqlalchemy.orm import Session
from db_engine import sync_engine
from models import User, Message


def seed_user_if_needed():
    with Session(sync_engine) as session:
        with session.begin():
            if session.query(User).get(1) is not None:
                print("User already exists, skipping seeding")
                return
            print("Seeding user")
            session.add(User(name="Alice"))
            session.add(User(name="AI"))
            session.commit()
