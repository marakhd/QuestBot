from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_classes_team_na_afffe5";
        ALTER TABLE "classes" DROP COLUMN "team_name";
        ALTER TABLE "users" ADD "full_name" VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP COLUMN "full_name";
        ALTER TABLE "classes" ADD "team_name" VARCHAR(255)  UNIQUE;
        CREATE UNIQUE INDEX "uid_classes_team_na_afffe5" ON "classes" ("team_name");"""
