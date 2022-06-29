-- upgrade --
CREATE TABLE IF NOT EXISTS "task" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "task_app" VARCHAR(100) NOT NULL,
    "task_env" VARCHAR(20) NOT NULL,
    "task_name" VARCHAR(100) NOT NULL,
    "task_status" VARCHAR(20) NOT NULL,
    "task_watermark" TIMESTAMPTZ NOT NULL,
    "task_duration" DOUBLE PRECISION,
    "task_metadata" JSONB,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "disabled" BOOL NOT NULL  DEFAULT False,
    "username" VARCHAR(100) NOT NULL UNIQUE,
    "email" VARCHAR(320) NOT NULL,
    "password_hash" VARCHAR(128),
    "category" VARCHAR(30) NOT NULL  DEFAULT 'misc',
    "full_name" VARCHAR(100),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
