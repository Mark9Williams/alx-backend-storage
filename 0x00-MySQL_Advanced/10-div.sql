-- Drop the function if it already exists
DROP FUNCTION IF EXISTS SafeDiv;

-- Create the SafeDiv function
DELIMITER $$

CREATE FUNCTION SafeDiv(a INT, b INT) 
RETURNS DECIMAL(10, 2)  -- The function returns a decimal value, adjust the precision if needed
DETERMINISTIC  -- Specifies that the function always returns the same result for the same inputs
BEGIN
    -- If b is 0, return 0, otherwise return a / b
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a / b;
    END IF;
END$$

DELIMITER ;
