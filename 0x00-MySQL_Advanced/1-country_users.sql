--  SQL script that creates a table users with id, email,name, and country columns.

-- Creates a table of users
CREATE TABLE IF NOT EXISTS users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255),
  country ENUM( 'US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
