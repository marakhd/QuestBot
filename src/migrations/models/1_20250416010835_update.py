from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "classes" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "state_game" INT NOT NULL  DEFAULT 0,
    "last_task_number" INT NOT NULL  DEFAULT 1,
    "start_time" TIMESTAMP,
    "is_active" INT NOT NULL  DEFAULT 1,
    "capitan_id" BIGINT REFERENCES "users" ("id") ON DELETE CASCADE,
    "last_task_id" BIGINT REFERENCES "questions" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "questions" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "data" TEXT,
    "text" TEXT NOT NULL,
    "correct_answer" TEXT NOT NULL,
    "answer_type" VARCHAR(255) NOT NULL,
    "is_active" INT NOT NULL  DEFAULT 1,
    "for_class_id" BIGINT REFERENCES "classes" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "scores" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "score" INT NOT NULL  DEFAULT 0,
    "class__id" BIGINT NOT NULL REFERENCES "classes" ("id") ON DELETE CASCADE,
    "quest_id" BIGINT NOT NULL REFERENCES "questions" ("id") ON DELETE RESTRICT
);
        CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "tg_username" VARCHAR(255)  UNIQUE,
    "tg_id" BIGINT NOT NULL UNIQUE,
    "full_name" VARCHAR(255),
    "sch_class_id" BIGINT NOT NULL REFERENCES "classes" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "questions";
        DROP TABLE IF EXISTS "scores";
        DROP TABLE IF EXISTS "classes";
        DROP TABLE IF EXISTS "users";"""
