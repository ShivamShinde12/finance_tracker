from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_role(x_user_role: str = Header('viewer')):
    if x_user_role not in {'admin', 'analyst', 'viewer'}:
        raise HTTPException(status_code=400, detail='Unknown role')
    return x_user_role


def require_role(required: str):
    def _requires(role: str = Depends(get_current_role)):
        order = {'viewer': 1, 'analyst': 2, 'admin': 3}
        if order[role] < order[required]:
            raise HTTPException(status_code=403, detail='Not authorized')
        return role
    return _requires


@router.post('/transactions', response_model=schemas.Transaction, dependencies=[Depends(require_role('admin'))])
def create_transaction(data: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, data)


@router.get('/transactions', response_model=list[schemas.Transaction], dependencies=[Depends(require_role('viewer'))])
def get_transactions(
    db: Session = Depends(get_db),
    type_: str | None = Query(None, alias='type'),
    category: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
):
    return crud.get_transactions(db, type=type_, category=category, start_date=start_date, end_date=end_date)


@router.get('/transactions/{transaction_id}', response_model=schemas.Transaction, dependencies=[Depends(require_role('viewer'))])
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    txn = crud.get_transaction(db, transaction_id)
    if not txn:
        raise HTTPException(status_code=404, detail='Transaction not found')
    return txn


@router.put('/transactions/{transaction_id}', response_model=schemas.Transaction, dependencies=[Depends(require_role('admin'))])
def update_transaction(transaction_id: int, data: schemas.TransactionUpdate, db: Session = Depends(get_db)):
    txn = crud.update_transaction(db, transaction_id, data)
    if not txn:
        raise HTTPException(status_code=404, detail='Transaction not found')
    return txn


@router.delete('/transactions/{transaction_id}', dependencies=[Depends(require_role('admin'))])
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_transaction(db, transaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Transaction not found')
    return {'message': 'deleted'}


@router.post('/users', response_model=schemas.User, dependencies=[Depends(require_role('admin'))])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.get('/users', response_model=list[schemas.User], dependencies=[Depends(require_role('analyst'))])
def get_all_users(db: Session = Depends(get_db)):
    return crud.get_users(db)
