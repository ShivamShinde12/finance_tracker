from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Transaction

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

@router.get("/summary")
def get_summary(db: Session = Depends(get_db), role: str = Depends(require_role('analyst'))):
    transactions = db.query(Transaction).all()

    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")

    return {
        "income": total_income,
        "expense": total_expense,
        "balance": total_income - total_expense
    }


@router.get('/analytics', dependencies=[Depends(require_role('analyst'))])
def get_analytics(db: Session = Depends(get_db)):
    txns = db.query(Transaction).all()
    total_income = sum(t.amount for t in txns if t.type == 'income')
    total_expense = sum(t.amount for t in txns if t.type == 'expense')
    balance = total_income - total_expense
    category_breakdown = {}
    for t in txns:
        category_breakdown.setdefault(t.category, 0)
        category_breakdown[t.category] += t.amount if t.type == 'income' else -t.amount
    sorted_by_date = sorted(txns, key=lambda t: t.date, reverse=True)
    recent = [{'id': t.id, 'amount': t.amount, 'type': t.type, 'category': t.category, 'date': t.date, 'notes': t.notes} for t in sorted_by_date[:10]]
    return {
        'summary': {'income': total_income, 'expense': total_expense, 'balance': balance},
        'category_breakdown': category_breakdown,
        'recent_activity': recent,
    }
