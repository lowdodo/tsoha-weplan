CREATE TABLE users(user_id SERIAL PRIMARY KEY, name TEXT, password TEXT);

CREATE TABLE plans(plan_id SERIAL PRIMARY KEY, creator_id INTEGER REFERENCES users, name TEXT, description TEXT, visible INTEGER);

CREATE TABLE subplans(subplans_id SERIAL PRIMARY KEY, plan_id INTEGER REFERENCES plans, creator_id INTEGER REFERENCES users, name TEXT, description TEXT, visible INTEGER); 

