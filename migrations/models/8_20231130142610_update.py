from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "accounts" ALTER COLUMN "type" SET DEFAULT 'staff';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "accounts" ALTER COLUMN "type" SET DEFAULT 'patient';"""
