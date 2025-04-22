from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "classes" ADD "last_task_id" BIGINT;
        CREATE TABLE IF NOT EXISTS "options" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "options" VARCHAR(255) NOT NULL,
    "option_text" TEXT NOT NULL,
    "question_id_id" BIGINT NOT NULL REFERENCES "questions" ("id") ON DELETE CASCADE
);
        ALTER TABLE "questions" ADD "for_class_id" BIGINT;
        CREATE TABLE IF NOT EXISTS "scores" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "score" INT NOT NULL  DEFAULT 0,
    "class__id" BIGINT NOT NULL REFERENCES "classes" ("id") ON DELETE CASCADE,
    "quest_id" BIGINT NOT NULL REFERENCES "questions" ("id") ON DELETE RESTRICT,
    "user_id" BIGINT REFERENCES "users" ("id") ON DELETE CASCADE
);
        ALTER TABLE "classes" ADD CONSTRAINT "fk_classes_question_392d0726" FOREIGN KEY ("last_task_id") REFERENCES "questions" ("id") ON DELETE CASCADE;
        ALTER TABLE "questions" ADD CONSTRAINT "fk_question_classes_46c6fd07" FOREIGN KEY ("for_class_id") REFERENCES "classes" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "questions" DROP CONSTRAINT IF EXISTS "fk_question_classes_46c6fd07";
        ALTER TABLE "classes" DROP CONSTRAINT IF EXISTS "fk_classes_question_392d0726";
        ALTER TABLE "classes" DROP COLUMN "last_task_id";
        ALTER TABLE "questions" DROP COLUMN "for_class_id";
        DROP TABLE IF EXISTS "scores";
        DROP TABLE IF EXISTS "options";"""
