from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "classes" ADD "capitan_id_id" BIGINT;
        ALTER TABLE "classes" ALTER COLUMN "team_name" TYPE VARCHAR(255) USING "team_name"::VARCHAR(255);
        ALTER TABLE "classes" ALTER COLUMN "name" TYPE VARCHAR(255) USING "name"::VARCHAR(255);
        ALTER TABLE "points" ADD "class__id" BIGINT NOT NULL;
        ALTER TABLE "points" ADD "quest_id" BIGINT NOT NULL;
        ALTER TABLE "quests" ADD "name" VARCHAR(255) NOT NULL UNIQUE;
        ALTER TABLE "quests" ADD "text" TEXT NOT NULL;
        ALTER TABLE "quests" ADD "answer" TEXT NOT NULL;
        ALTER TABLE "users" ALTER COLUMN "tg_username" TYPE VARCHAR(255) USING "tg_username"::VARCHAR(255);
        ALTER TABLE "classes" ADD CONSTRAINT "fk_classes_users_b555a9e7" FOREIGN KEY ("capitan_id_id") REFERENCES "users" ("id") ON DELETE CASCADE;
        ALTER TABLE "points" ADD CONSTRAINT "fk_points_classes_a91077fb" FOREIGN KEY ("class__id") REFERENCES "classes" ("id") ON DELETE CASCADE;
        ALTER TABLE "points" ADD CONSTRAINT "fk_points_quests_73f54155" FOREIGN KEY ("quest_id") REFERENCES "quests" ("id") ON DELETE CASCADE;
        CREATE UNIQUE INDEX "uid_quests_name_868e9e" ON "quests" ("name");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_quests_name_868e9e";
        ALTER TABLE "points" DROP CONSTRAINT IF EXISTS "fk_points_quests_73f54155";
        ALTER TABLE "points" DROP CONSTRAINT IF EXISTS "fk_points_classes_a91077fb";
        ALTER TABLE "classes" DROP CONSTRAINT IF EXISTS "fk_classes_users_b555a9e7";
        ALTER TABLE "users" ALTER COLUMN "tg_username" TYPE VARCHAR(255) USING "tg_username"::VARCHAR(255);
        ALTER TABLE "classes" DROP COLUMN "capitan_id_id";
        ALTER TABLE "classes" ALTER COLUMN "team_name" TYPE VARCHAR(255) USING "team_name"::VARCHAR(255);
        ALTER TABLE "classes" ALTER COLUMN "name" TYPE VARCHAR(255) USING "name"::VARCHAR(255);
        ALTER TABLE "points" DROP COLUMN "class__id";
        ALTER TABLE "points" DROP COLUMN "quest_id";
        ALTER TABLE "quests" DROP COLUMN "name";
        ALTER TABLE "quests" DROP COLUMN "text";
        ALTER TABLE "quests" DROP COLUMN "answer";"""
