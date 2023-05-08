import os

from app.api import endpoints, ping
from app.db import generate_schema, init_db
from app.load_data import insert_records, load_csv
from app.logger import uvicorn_logger
from app.models.models import Ship
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

DATA_PATH = os.path.join(os.path.dirname(__file__), "data/output.csv")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application instance.

    Returns:
        A FastAPI application instance.
    """
    application = FastAPI()

    register_tortoise(
        application,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )

    application.include_router(ping.router)
    application.include_router(endpoints.router)

    return application


app = create_application()
records = load_csv(DATA_PATH)


@app.on_event("startup")
async def startup_event():
    """Event handler for starting up the application.

    Initializes the database connection pool and inserts records into the database.
    """
    uvicorn_logger.info("Starting up...")
    init_db(app)
    await generate_schema()
    record_count = await Ship.all().count()
    if record_count == 0:
        await insert_records(records)


@app.on_event("shutdown")
async def shutdown_event():
    """Event handler for shutting down the application.

    Logs a message indicating that the application is shutting down.
    """
    uvicorn_logger.info("Shutting down...")

