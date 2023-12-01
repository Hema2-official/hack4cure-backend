from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "document" ADD "data" JSONB;
        ALTER TABLE "document" ADD "pdf" BYTEA;
        DROP TABLE IF EXISTS "pdf";
        DROP TABLE IF EXISTS "formsubmission";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "document" DROP COLUMN "data";
        ALTER TABLE "document" DROP COLUMN "pdf";"""
