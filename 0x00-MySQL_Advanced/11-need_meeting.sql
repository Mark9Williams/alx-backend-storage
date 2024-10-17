-- Drop the view if it already exists
DROP VIEW IF EXISTS need_meeting;

-- Create the view need_meeting
CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80  -- Condition for students with scores strictly less than 80
AND (
    last_meeting IS NULL  -- No last_meeting date
    OR last_meeting < DATE_SUB(CURDATE(), INTERVAL 1 MONTH)  -- Last meeting was more than a month ago
);
