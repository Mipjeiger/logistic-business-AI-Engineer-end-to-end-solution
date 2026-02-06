from fastapi import FastAPI
from app.routers import tabular, yolo, rag

def create_app() -> FastAPI:
    app = FastAPI(
        title="MLOps Platform API",
        version="1.0.0",
    )

    # Register routers only
    app.include_router(tabular.router)
    app.include_router(rag.router)
    app.include_router(yolo.router)

    return app

# ASGI entry point
app = create_app()