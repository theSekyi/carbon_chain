from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "ship" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "ship_type" VARCHAR(255) NOT NULL,
    "reporting_period" DATE NOT NULL,
    "doc_issue_date" DATE NOT NULL,
    "doc_expiry_date" DATE NOT NULL,
    "annual_average_co2_emissions_per_distance" DOUBLE PRECISION NOT NULL,
    "total_co2_emissions" DOUBLE PRECISION NOT NULL,
    "technical_efficiency" DOUBLE PRECISION NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
