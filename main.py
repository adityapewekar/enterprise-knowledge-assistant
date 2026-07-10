
from fastapi import FastAPI
from presentation.api.controllers.ask_controller import router as presentation_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(presentation_router)

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