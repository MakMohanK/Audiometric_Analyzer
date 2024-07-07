-- schema.sql

-- CREATE TABLE IF NOT EXISTS users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     email TEXT UNIQUE NOT NULL,
--     password TEXT NOT NULL
-- );

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    age INTEGER,
    dob DATE,
    mobile_number TEXT
);