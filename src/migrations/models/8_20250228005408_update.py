from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "scores" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "score" INT NOT NULL  DEFAULT 0,
    "class__id" BIGINT NOT NULL REFERENCES "classes" ("id") ON DELETE CASCADE,
    "quest_id" BIGINT NOT NULL REFERENCES "quests" ("id") ON DELETE CASCADE
);
        DROP TABLE IF EXISTS "points";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "scores";"""
