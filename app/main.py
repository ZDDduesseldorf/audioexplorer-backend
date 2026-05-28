from fastapi import FastAPI

from app.api.sound_controller import router as sound_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Audioexplorer API",
        version="0.1.0",
        description="Backend API for the Audioexplorer application.",
    )

    app.include_router(sound_router, prefix="/api/v1")

    return app


app = create_app()
