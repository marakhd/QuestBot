from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "classes" RENAME COLUMN "last_task" TO "last_task_number";
        ALTER TABLE "classes" ADD "last_task_id" BIGINT;
        ALTER TABLE "classes" ADD CONSTRAINT "fk_classes_quests_689a0ee7" FOREIGN KEY ("last_task_id") REFERENCES "quests" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "classes" DROP CONSTRAINT IF EXISTS "fk_classes_quests_689a0ee7";
        ALTER TABLE "classes" RENAME COLUMN "last_task_number" TO "last_task";
        ALTER TABLE "classes" DROP COLUMN "last_task_id";"""
