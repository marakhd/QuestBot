from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP CONSTRAINT IF EXISTS "fk_users_classes_aca8b81a";
        ALTER TABLE "classes" DROP CONSTRAINT IF EXISTS "fk_classes_users_b555a9e7";
        ALTER TABLE "classes" RENAME COLUMN "capitan_id_id" TO "capitan_id";
        ALTER TABLE "users" RENAME COLUMN "class_id_id" TO "sch_class_id";
        ALTER TABLE "classes" ADD CONSTRAINT "fk_classes_users_25e12993" FOREIGN KEY ("capitan_id") REFERENCES "users" ("id") ON DELETE CASCADE;
        ALTER TABLE "users" ADD CONSTRAINT "fk_users_classes_21c1f1cb" FOREIGN KEY ("sch_class_id") REFERENCES "classes" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "classes" DROP CONSTRAINT IF EXISTS "fk_classes_users_25e12993";
        ALTER TABLE "users" DROP CONSTRAINT IF EXISTS "fk_users_classes_21c1f1cb";
        ALTER TABLE "users" RENAME COLUMN "sch_class_id" TO "class_id_id";
        ALTER TABLE "classes" RENAME COLUMN "capitan_id" TO "capitan_id_id";
        ALTER TABLE "users" ADD CONSTRAINT "fk_users_classes_aca8b81a" FOREIGN KEY ("class_id_id") REFERENCES "classes" ("id") ON DELETE CASCADE;
        ALTER TABLE "classes" ADD CONSTRAINT "fk_classes_users_b555a9e7" FOREIGN KEY ("capitan_id_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""
