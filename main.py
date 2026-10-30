
from fastapi import FastAPI
from presentation.api.controllers.ask_controller import ask_router
from presentation.api.controllers.kb_controller import kb_router
from presentation.api.controllers.token_controller import token_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Enterprise Knowledge Assistant API",
    description="AI-powered knowledge management system with token tracking and management",
    version="1.0.0"
)
app.include_router(ask_router)
app.include_router(kb_router)
app.include_router(token_router)


# Allow your Angular dev server (default: http://localhost:4200)
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # ✅ which origins can call your API
    allow_credentials=True,
    allow_methods=["*"],            # ✅ allow GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],            # ✅ allow all headers (Content-Type, Authorization, etc.)
)