from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "quests" ALTER COLUMN "data" TYPE TEXT USING "data"::TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "quests" ALTER COLUMN "data" TYPE VARCHAR(255) USING "data"::VARCHAR(255);"""
