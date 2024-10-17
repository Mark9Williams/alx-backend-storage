-- --  a SQL script that creates a trigger that decreases the quantity of an item after adding a new order.

-- -- Initial setup: Drop tables if they exist
-- DROP TABLE IF EXISTS items;
-- DROP TABLE IF EXISTS orders;

-- -- Create the items table
-- CREATE TABLE IF NOT EXISTS items (
--     name VARCHAR(255) NOT NULL,
--     quantity INT NOT NULL DEFAULT 10
-- );

-- -- Create the orders table
-- CREATE TABLE IF NOT EXISTS orders (
--     item_name VARCHAR(255) NOT NULL,
--     number INT NOT NULL
-- );

-- -- Insert some initial data into the items table
-- INSERT INTO items (name) VALUES ("apple"), ("pineapple"), ("pear");

-- Create the trigger to decrease the quantity after an order is placed
DELIMITER $$

CREATE TRIGGER decrease_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END$$

DELIMITER ;
