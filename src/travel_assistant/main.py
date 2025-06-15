from fastapi import FastAPI
from travel_assistant.api.routes import router
from dotenv import load_dotenv
from travel_assistant.core.logging import setup_logging

# Load environment variables
load_dotenv()
setup_logging()

# initialize FastAPI app
app = FastAPI(
    title="VAA GenAI Travel Assistant",
    description="Production-grade travel advice grounded in seed data",
    version="0.1.0",
)

# include API routes
app.include_router(router)


@app.get("/", summary="Root endpoint")
def read_root():
    """Return a welcome message for the API."""
    return {"message": "Travel Assistant API is running"}


@app.get("/health", summary="Health check endpoint")
def health_check():
    """Return the health status of the API."""
    return {"status": "healthy"}
