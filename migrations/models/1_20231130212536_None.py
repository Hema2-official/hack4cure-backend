from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "account" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(254)  UNIQUE,
    "password" TEXT,
    "google_id" TEXT,
    "first_name" TEXT,
    "last_name" TEXT,
    "created_at" INT NOT NULL,
    "updated_at" INT NOT NULL,
    "type" VARCHAR(7) NOT NULL  DEFAULT 'staff'
);
COMMENT ON COLUMN "account"."type" IS 'PATIENT: patient\nSTAFF: staff';
CREATE TABLE IF NOT EXISTS "form" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "fields" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "document" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "timestamp" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "file_path" TEXT NOT NULL,
    "account_id" INT NOT NULL REFERENCES "account" ("id") ON DELETE CASCADE,
    "form_id" INT NOT NULL REFERENCES "form" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "formsubmission" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "timestamp" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "file_path" TEXT NOT NULL,
    "data" JSONB NOT NULL,
    "account_id" INT NOT NULL REFERENCES "account" ("id") ON DELETE CASCADE,
    "form_id" INT NOT NULL REFERENCES "form" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "log" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "timestamp" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "text" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "pdf" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "timestamp" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "file_path" TEXT NOT NULL,
    "file" BYTEA NOT NULL,
    "account_id" INT NOT NULL REFERENCES "account" ("id") ON DELETE CASCADE,
    "form_id" INT NOT NULL REFERENCES "form" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
