from fastapi import FastAPI
from .routers import image_classification_router
from .config import setup_logging
setup_logging("DEBUG")  # Set the desired log level here, e.g., "DEBUG

app = FastAPI(
    title="AI Tools API",
    description="API for various AI tools",
    version="1.0.0",
    root_path="/api/v1/ai",
)

app.include_router(image_classification_router)

