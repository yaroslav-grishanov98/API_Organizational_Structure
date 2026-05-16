import logging
from fastapi import FastAPI
from app.routers.departments import router as departments_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="Организационная структура АПИ",
    description="АПИ для управления организационной структуры компании",
    version="1.0.0",
)

app.include_router(departments_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
