from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "quests" ALTER COLUMN "for_class_id" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "quests" ALTER COLUMN "for_class_id" SET NOT NULL;"""
