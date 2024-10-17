-- Create a trigger that resets the valid_email attribute when the email is changed

DELIMITER $$  -- Change the delimiter to allow for multi-line statements

CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users  -- Trigger will fire before an update on the users table
FOR EACH ROW
BEGIN
    -- Check if the email has changed
    IF OLD.email <> NEW.email THEN
        -- Reset valid_email if the email has changed
        SET NEW.valid_email = 0;  -- Or use FALSE if valid_email is a boolean
    END IF;
END$$

DELIMITER ;  -- Reset the delimiter back to default
