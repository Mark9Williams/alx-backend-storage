-- Create a stored procedure AddBonus that adds a new correction for a student

DELIMITER $$  -- Change the delimiter to allow for multi-line statements

CREATE PROCEDURE AddBonus (
    IN user_id INT,            -- User ID (linked to an existing user in users table)
    IN project_name VARCHAR(255), -- Project name (new or already exists)
    IN score INT               -- Score value for the correction
)
BEGIN
    DECLARE project_id INT;   -- Variable to hold the project ID

    -- Check if the project already exists
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name;

    -- If the project does not exist, create it
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();  -- Get the ID of the newly created project
    END IF;

    -- Insert the correction into the corrections table
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score);
END$$

DELIMITER ;  -- Reset the delimiter back to default
