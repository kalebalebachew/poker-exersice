"""Main FastAPI application."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import yaml

from app.api.endpoints import hands
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for evaluating poker hands and managing poker games",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hands.router, prefix=f"{settings.API_V1_STR}/poker")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the Poker Hand Evaluator API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


def custom_openapi():
    """Generate custom OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema

    # Check if we have a pre-defined OpenAPI schema
    openapi_path = os.path.join(os.path.dirname(__file__), "api", "openapi.yaml")
    if os.path.exists(openapi_path):
        with open(openapi_path, "r") as f:
            openapi_schema = yaml.safe_load(f)
            app.openapi_schema = openapi_schema
            return app.openapi_schema

    # Otherwise, generate it from the code
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Customize the schema
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi 