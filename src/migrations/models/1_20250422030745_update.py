from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "classes" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "state_game" BOOL NOT NULL  DEFAULT False,
    "last_task_number" INT NOT NULL  DEFAULT 1,
    "start_time" TIMESTAMPTZ,
    "is_active" BOOL NOT NULL  DEFAULT True
);
        CREATE TABLE IF NOT EXISTS "questions" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "data" TEXT,
    "grade_group" VARCHAR(25) NOT NULL,
    "text" TEXT NOT NULL,
    "correct_answer" TEXT NOT NULL,
    "answer_type" VARCHAR(255) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True
);
        CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "tg_username" VARCHAR(255)  UNIQUE,
    "tg_id" BIGINT NOT NULL UNIQUE,
    "full_name" VARCHAR(255),
    "sch_class_id" BIGINT NOT NULL REFERENCES "classes" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "classes";
        DROP TABLE IF EXISTS "questions";
        DROP TABLE IF EXISTS "users";"""
