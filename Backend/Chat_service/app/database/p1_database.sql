CREATE DATABASE IF NOT EXISTS p1_database;

USE p1_database;

CREATE TABLE IF NOT EXISTS conversations (
    convo_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    participants JSON NOT NULL,  -- Assuming participants are stored as a JSON array
    messages JSON DEFAULT NULL,    -- Assuming messages are stored as a JSON array
    isGroup BOOLEAN NOT NULL DEFAULT FALSE
);