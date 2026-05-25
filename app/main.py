# app/main.py

from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users, assets

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API REST de Gestão de Arquivos")

app.include_router(users.router, prefix="/auth", tags=["Auth"])
app.include_router(assets.router, prefix="/assets", tags=["Assets"])

@app.get("/")
def health_check():
    return {"status": "API online"}