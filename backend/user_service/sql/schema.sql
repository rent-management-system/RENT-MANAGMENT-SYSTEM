-- SQL schema for the users table
CREATE TYPE userrole AS ENUM ('admin', 'owner', 'tenant', 'broker');
CREATE TYPE language AS ENUM ('en', 'am', 'om');
CREATE TYPE currency AS ENUM ('ETB', 'USD');

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR,
    full_name VARCHAR NOT NULL,
    role userrole NOT NULL DEFAULT 'tenant',
    phone_number BYTEA,
    preferred_language language DEFAULT 'en',
    preferred_currency currency DEFAULT 'ETB',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    password_changed BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_user_id ON users (id);
CREATE INDEX idx_user_email ON users (email);
CREATE INDEX idx_user_role ON users (role);
