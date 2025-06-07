from fastapi import FastAPI
from app.routes import router
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Levo Schema API")
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Levo Schema API is up and running 🚀"}
