
from fastapi import FastAPI
from presentation.api import router as presentation_router


app = FastAPI()
app.include_router(presentation_router)
