-- WellMind Database Initialization Script
-- This script creates the necessary database and tables for the WellMind application

-- Create database (skip if using Render's managed database)
-- CREATE DATABASE IF NOT EXISTS chatbot;
-- USE chatbot;

-- Create users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username)
);

-- Optional: Insert a default admin user for testing
-- Note: This is a plain text password. Consider implementing password hashing in production.
-- INSERT INTO users (username, password) VALUES ('admin', '123456')
-- ON DUPLICATE KEY UPDATE username=username;
