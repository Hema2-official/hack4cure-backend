from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "accounts" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(254)  UNIQUE,
    "email_verified" BOOL NOT NULL  DEFAULT False,
    "password" TEXT,
    "google_id" TEXT,
    "first_name" TEXT,
    "last_name" TEXT,
    "created_at" INT NOT NULL,
    "updated_at" INT NOT NULL,
    "type" VARCHAR(7) NOT NULL  DEFAULT 'staff',
    "gender" VARCHAR(6)
);
COMMENT ON COLUMN "accounts"."type" IS 'PATIENT: patient\nSTAFF: staff';
COMMENT ON COLUMN "accounts"."gender" IS 'MALE: male\nFEMALE: female';
CREATE TABLE IF NOT EXISTS "demands" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "cancer_type" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "fractions" INT NOT NULL,
    "is_inpatient" BOOL NOT NULL,
    "weight" DOUBLE PRECISION NOT NULL,
    "patient_id" INT NOT NULL REFERENCES "accounts" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "logs" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "timestamp" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "text" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "maintenanceevent" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "start" TIMESTAMPTZ NOT NULL,
    "duration" INT NOT NULL,
    "resource_id" INT NOT NULL,
    "display_name" TEXT,
    "color" TEXT
);
CREATE TABLE IF NOT EXISTS "resources" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type" TEXT NOT NULL,
    "status" VARCHAR(11) NOT NULL  DEFAULT 'operating'
);
COMMENT ON COLUMN "resources"."status" IS 'MAINTENANCE: maintenance\nOPERATING: operating';
CREATE TABLE IF NOT EXISTS "rooms" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "gender" VARCHAR(6) NOT NULL,
    "capacity" INT NOT NULL  DEFAULT 0
);
COMMENT ON COLUMN "rooms"."gender" IS 'MALE: male\nFEMALE: female';
CREATE TABLE IF NOT EXISTS "appointments" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "start" TIMESTAMPTZ NOT NULL,
    "end" TIMESTAMPTZ NOT NULL,
    "demand_id" INT NOT NULL REFERENCES "demands" ("id") ON DELETE CASCADE,
    "resource_id" INT NOT NULL REFERENCES "resources" ("id") ON DELETE CASCADE,
    "room_id" INT REFERENCES "rooms" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_appointment_resourc_286f64" UNIQUE ("resource_id", "start"),
    CONSTRAINT "uid_appointment_resourc_03aa82" UNIQUE ("resource_id", "end")
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
