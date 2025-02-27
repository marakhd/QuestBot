from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "classes" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "team_name" VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "points" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS "quests" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "tg_username" VARCHAR(255) NOT NULL UNIQUE,
    "tg_id" BIGINT NOT NULL UNIQUE,
    "class_id_id" BIGINT NOT NULL REFERENCES "classes" ("id") ON DELETE CASCADE
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
