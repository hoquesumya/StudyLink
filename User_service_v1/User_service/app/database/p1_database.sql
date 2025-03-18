CREATE database if not exists p1_database;

USE p1_database;

USE  p1_database;

CREATE TABLE IF NOT EXISTS user_profiles (
    user_id VARCHAR(50) PRIMARY KEY,
    canvas_token TEXT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    short_name VARCHAR(50) DEFAULT NULL,
    email VARCHAR(100) NOT NULL,
    pronouns VARCHAR(50) DEFAULT NULL,
    courses TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);