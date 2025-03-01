from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "classes" ADD "state_game" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "classes" ADD "last_task" INT NOT NULL  DEFAULT 1;
        ALTER TABLE "quests" ADD "for_class_id" BIGINT NOT NULL;
        ALTER TABLE "quests" ADD CONSTRAINT "fk_quests_classes_6ab95588" FOREIGN KEY ("for_class_id") REFERENCES "classes" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "quests" DROP CONSTRAINT IF EXISTS "fk_quests_classes_6ab95588";
        ALTER TABLE "classes" DROP COLUMN "state_game";
        ALTER TABLE "classes" DROP COLUMN "last_task";
        ALTER TABLE "quests" DROP COLUMN "for_class_id";"""
