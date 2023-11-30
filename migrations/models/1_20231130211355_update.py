from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "accounts" DROP COLUMN "email_verified";
        ALTER TABLE "accounts" DROP COLUMN "gender";
        CREATE TABLE IF NOT EXISTS "documents" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "timestamp" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "file_path" TEXT NOT NULL,
    "account_id" INT NOT NULL REFERENCES "accounts" ("id") ON DELETE CASCADE,
    "form_id" INT NOT NULL REFERENCES "form" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "form" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "fields" JSONB NOT NULL
);
        CREATE TABLE IF NOT EXISTS "form_submissions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "timestamp" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "file_path" TEXT NOT NULL,
    "data" JSONB NOT NULL,
    "account_id" INT NOT NULL REFERENCES "accounts" ("id") ON DELETE CASCADE,
    "form_id" INT NOT NULL REFERENCES "form" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "pdfs" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "timestamp" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "file_path" TEXT NOT NULL,
    "file" BYTEA NOT NULL,
    "account_id" INT NOT NULL REFERENCES "accounts" ("id") ON DELETE CASCADE,
    "form_id" INT NOT NULL REFERENCES "form" ("id") ON DELETE CASCADE
);
        DROP TABLE IF EXISTS "rooms";
        DROP TABLE IF EXISTS "demands";
        DROP TABLE IF EXISTS "resources";
        DROP TABLE IF EXISTS "appointments";
        DROP TABLE IF EXISTS "maintenanceevent";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "accounts" ADD "email_verified" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "accounts" ADD "gender" VARCHAR(6);
        DROP TABLE IF EXISTS "documents";
        DROP TABLE IF EXISTS "form";
        DROP TABLE IF EXISTS "form_submissions";
        DROP TABLE IF EXISTS "pdfs";"""
