-- script that creates a stored procedure ComputeAverageWeightedScoreForUsers.
-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Change the delimiter to avoid issues with semicolons in the procedure
DELIMITER //

-- Create the ComputeAverageWeightedScoreForUsers procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id INT;
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE weighted_average FLOAT;

    -- Declare a cursor to iterate over all users
    DECLARE user_cursor CURSOR FOR 
        SELECT id FROM users;

    -- Declare a handler to exit the loop
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- Open the cursor
    OPEN user_cursor;

    -- Loop through all users
    read_loop: LOOP
        FETCH user_cursor INTO user_id;

        -- Exit loop if no more users
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Initialize total_score and total_weight
        SET total_score = 0;
        SET total_weight = 0;

        -- Calculate total score and total weight for the current user
        SELECT 
            COALESCE(SUM(c.score * p.weight), 0),  -- If no results, default to 0
            COALESCE(SUM(p.weight), 0)
        INTO 
            total_score, total_weight
        FROM 
            corrections c
        JOIN 
            projects p ON c.project_id = p.id
        WHERE 
            c.user_id = user_id;

        -- Calculate the weighted average if total_weight is greater than 0
        IF total_weight > 0 THEN
            SET weighted_average = total_score / total_weight;
        ELSE
            SET weighted_average = 0; -- No scores, set average to 0
        END IF;

        -- Update the user's average score in the users table
        UPDATE users SET average_score = weighted_average WHERE id = user_id;
    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END//

-- Restore the delimiter to the default
DELIMITER ;
