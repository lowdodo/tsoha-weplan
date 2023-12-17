CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT
);

CREATE TABLE plans (
    plan_id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users(user_id),
    creator_name TEXT REFERENCES users(name),
    name TEXT,
    description TEXT,
    visible INTEGER,
    is_done BOOLEAN
);

CREATE TABLE subplans (
    subplans_id SERIAL PRIMARY KEY,
    plan_id INTEGER REFERENCES plans(plan_id),
    creator_id INTEGER REFERENCES users(user_id),
    creator_name TEXT REFERENCES users(name),
    name TEXT,
    description TEXT,
    visible INTEGER,
    is_done BOOLEAN
);

CREATE TABLE ownplans (
    user_plan_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    plan_id INTEGER REFERENCES plans(plan_id),
    creator_name TEXT REFERENCES users(name),
    visible INTEGER,
    is_done BOOLEAN
);

CREATE TABLE comments(
    comment_id SERIAL PRIMARY KEY,
    plan_id INTEGER REFERENCES plans(plan_id),
    username TEXT REFERENCES users(name),
    comment TEXT,
    visible INTEGER,
    is_done BOOLEAN,
    created_at TIMESTAMP
);