-- Create a stored procedure ComputeAverageScoreForUser that computes and stores the average score for a student

DELIMITER $$  -- Change the delimiter to allow for multi-line statements

CREATE PROCEDURE ComputeAverageScoreForUser (
    IN user_id INT  -- User ID (linked to an existing user in the users table)
)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);  -- Variable to hold the average score

    -- Calculate the average score from the corrections table for the given user_id
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    -- Update the average_score column in the users table
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END$$

DELIMITER ;  -- Reset the delimiter back to default
