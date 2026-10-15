from fastapi import FastAPI

from interfaces.auth_routes import router as auth_router
from interfaces.crud_routes import router as crud_router


app = FastAPI(title="Khaojai Python Backend")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(crud_router)