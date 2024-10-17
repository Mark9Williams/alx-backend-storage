-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Change the delimiter to avoid issues with semicolons in the procedure
DELIMITER //

-- Create the ComputeAverageWeightedScoreForUser procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;
    DECLARE weighted_average FLOAT DEFAULT 0;

    -- Calculate the total score and total weight for the given user_id
    SELECT 
        SUM(c.score * p.weight) INTO total_score
    FROM 
        corrections c
    JOIN 
        projects p ON c.project_id = p.id
    WHERE 
        c.user_id = user_id;

    SELECT 
        SUM(p.weight) INTO total_weight
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
END//

-- Restore the delimiter to the default
DELIMITER ;
