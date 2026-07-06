
from fastapi import FastAPI
from Presentation.api import router as presentation_router


app = FastAPI()
app.include_router(presentation_router)
