from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from db.models import User
from utils.settings import ENV_PATH

load_dotenv(ENV_PATH)


# Database funksiyalari
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()


def create_user(db: Session, user_id: int, username: str, full_name: str, invited_by: int = None):
    user = User(
        user_id=user_id,
        username=username,
        full_name=full_name,
        invited_by=invited_by
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def increment_conversion(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        user.conversion_count += 1
        user.last_conversion = datetime.now()
        db.commit()
        return user.conversion_count
    return 0


def check_and_block_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if user and user.conversion_count >= 5:
        user.is_blocked = True
        db.commit()
        return True
    return False


def unblock_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        user.is_blocked = False
        user.conversion_count = 0
        db.commit()


def add_invited_user(db: Session, inviter_id: int):
    user = get_user(db, inviter_id)
    if user:
        user.invited_count += 1
        db.commit()
        return user.invited_count
    return 0
