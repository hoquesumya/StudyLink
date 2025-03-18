# COMS-4153-Project-Chat-Microservice

The Chat Microservice allows students to communicate with one another via text messages. Below are the functionalities available.

## Create new conversation

Send POST request to /conversations/ with JSON body

{
  "name": "Coding Workshop",
  "participants": ["John Doe", "Jane Smith", "Bob Johnson", "CurrentUser"],
  "messages": [{ "text": "Welcome to our project group!", "sender": "CurrentUser", "timestamp": "9:00 AM" }],
  "isGroup": true
}

## Update conversation details

Send PUT request to /conversations/{conversation_id} with JSON body

{
  "name": "Coding Workshop",
  "participants": ["John Doe", "Jane Smith", "Bob Johnson", "CurrentUser"],
  "messages": [{ "text": "Welcome to our project group!", "sender": "CurrentUser", "timestamp": "9:00 AM" }, { "text": "Hi guys!", "sender": "Jane Smith", "timestamp": "3:00 PM" }],
  "isGroup": true
}

## Get converstaion details

Send GET request to /conversations/{conversation_id}

## DELETE converstaion details

Send DELETE request to /conversations/{conversation_id}

## Conversation database:

CREATE DATABASE IF NOT EXISTS p1_database;

USE p1_database;

CREATE TABLE IF NOT EXISTS conversations (
    convo_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    participants JSON NOT NULL,  
    messages JSON DEFAULT NULL, 
    isGroup BOOLEAN NOT NULL DEFAULT FALSE
);