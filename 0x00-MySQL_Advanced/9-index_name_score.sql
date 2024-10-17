-- a SQL script that creates an index idx_name_first_score on the table names and the first letter of name and the score.
-- Create a composite index on the first letter of 'name' and the 'score' column
CREATE INDEX idx_name_first_score ON names (name(1), score);
