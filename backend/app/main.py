from fastapi import FastAPI
from app.api.v1.emergency_ws import router as emergency_router

app = FastAPI(title="AetherDoc Emergency AI")

app.include_router(emergency_router)
