from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import transaction, analytics

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
	return {"message": "Finance Tracker API is running"}

app.include_router(transaction.router)
app.include_router(analytics.router)
