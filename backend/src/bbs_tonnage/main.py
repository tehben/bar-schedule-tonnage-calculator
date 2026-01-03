from fastapi import FastAPI
from bbs_tonnage.api.routes import router

app = FastAPI(title="Bar Schedule Tonnage API", version="0.1.0")

@app.get("/")
def root():
    return {"service": "bbs-tonnage", "docs": "/docs", "health": "/health"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router)
