from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes import mental_chat, mental_session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AetherDoc Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(mental_session.router)
app.include_router(mental_chat.router)

@app.get("/")
def root():
    return {"status": "AetherDoc backend running"}
