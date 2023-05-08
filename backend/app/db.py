import logging
import os

from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

log = logging.getLogger("uvicorn")


TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {"models": {"models": ["app.models.models", "aerich.models"], "default_connection": "default",},},
}


def init_db(app: FastAPI) -> None:
    """
    Initialize the Tortoise ORM connection and register it with a FastAPI application.
    Args:
        app (FastAPI): The FastAPI application instance to register the Tortoise ORM with.
    Returns:
        None
    """

    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def generate_schema() -> None:
    """Generate the database schema based on the defined models in the application.
    This function initializes the Tortoise ORM, generates the schema for the models, and then closes the database connections.

    Returns:
        None
    """

    log.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"), modules={"models": ["app.models.models"]},
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())
