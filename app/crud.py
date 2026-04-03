from sqlalchemy.orm import Session
from app import models

def create_transaction(db: Session, data):
    txn = models.Transaction(**data.dict())
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


def get_transaction(db: Session, transaction_id: int):
    txn = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if txn:
        return {'id': txn.id, 'amount': txn.amount, 'type': txn.type, 'category': txn.category, 'date': txn.date, 'notes': txn.notes}
    return None


def get_transactions(db: Session, type: str = None, category: str = None, start_date=None, end_date=None):
    query = db.query(models.Transaction)
    if type is not None:
        query = query.filter(models.Transaction.type == type)
    if category is not None:
        query = query.filter(models.Transaction.category == category)
    if start_date is not None:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date is not None:
        query = query.filter(models.Transaction.date <= end_date)
    txns = query.order_by(models.Transaction.date.desc()).all()
    return txns


def update_transaction(db: Session, transaction_id: int, data):
    txn = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not txn:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(txn, field, value)
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return {'id': txn.id, 'amount': txn.amount, 'type': txn.type, 'category': txn.category, 'date': txn.date, 'notes': txn.notes}


def delete_transaction(db: Session, transaction_id: int):
    txn = get_transaction(db, transaction_id)
    if not txn:
        return False
    db.delete(txn)
    db.commit()
    return True


def create_user(db: Session, user_data):
    user = models.User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):
    return db.query(models.User).all()

def get_transactions(db: Session):
    return db.query(models.Transaction).all()
