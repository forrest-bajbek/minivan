-- upgrade --
CREATE TABLE IF NOT EXISTS "task" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "task_app" VARCHAR(100) NOT NULL,
    "task_env" VARCHAR(4) NOT NULL,
    "task_name" VARCHAR(100) NOT NULL,
    "task_status" VARCHAR(8) NOT NULL,
    "task_watermark" TIMESTAMPTZ NOT NULL,
    "task_duration" DOUBLE PRECISION,
    "task_metadata" JSONB,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "task"."task_env" IS 'PROD: prod\nSTG: stg\nDEV: dev';
COMMENT ON COLUMN "task"."task_status" IS 'START: start\nCOMPLETE: complete\nFAIL: fail';
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(100) NOT NULL UNIQUE,
    "password_hash" VARCHAR(128) NOT NULL,
    "email" VARCHAR(320) NOT NULL,
    "full_name" VARCHAR(100),
    "category" VARCHAR(5) NOT NULL,
    "is_admin" BOOL NOT NULL  DEFAULT False,
    "is_disabled" BOOL NOT NULL  DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "user"."category" IS 'HUMAN: human\nROBOT: robot';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
