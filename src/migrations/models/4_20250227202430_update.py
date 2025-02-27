from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "quests" ADD "is_active" BOOL NOT NULL  DEFAULT True;
        ALTER TABLE "quests" ADD "type" VARCHAR(255) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "quests" DROP COLUMN "is_active";
        ALTER TABLE "quests" DROP COLUMN "type";"""
