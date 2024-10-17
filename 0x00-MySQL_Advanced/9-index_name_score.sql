-- Create an index idx_name_first_score on the first letter of the name column and the score column in the names table

-- Make sure to adjust the database context if needed
USE your_database_name;  -- Replace with the actual name of your database

-- Create the index
CREATE INDEX idx_name_first_score ON names (SUBSTRING(name, 1, 1), score);