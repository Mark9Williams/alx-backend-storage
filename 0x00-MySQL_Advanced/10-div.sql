-- a SQL script that creates a function SafeDiv that handles division by zero.
-- Change the delimiter to something else (e.g., //)
DELIMITER //

-- Drop the function if it already exists
DROP FUNCTION IF EXISTS SafeDiv//

-- Create the SafeDiv function
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    -- Check if the second number (b) is 0
    IF b = 0 THEN
        RETURN 0; -- Return 0 if b is 0
    ELSE
        RETURN a / b; -- Otherwise return a / b
    END IF;
END//

-- Change the delimiter back to semicolon
DELIMITER ;
