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
    visible INTEGER
);

CREATE TABLE subplans (
    subplans_id SERIAL PRIMARY KEY,
    plan_id INTEGER REFERENCES plans(plan_id),
    creator_id INTEGER REFERENCES users(user_id),
    creator_name TEXT REFERENCES users(name),
    name TEXT,
    description TEXT,
    visible INTEGER
);

CREATE TABLE priority (
    priority_id SERIAL PRIMARY KEY,
    plan_id INTEGER REFERENCES plans(plan_id),
    creator_id INTEGER REFERENCES users(user_id), 
    name INTEGER REFERENCES plans(plan_id),
    visible INTEGER
);


CREATE TABLE ownplans (
    user_plan_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    plan_id INTEGER REFERENCES plans(plan_id),
    creator_name TEXT REFERENCES users(name),
    visible INTEGER
);