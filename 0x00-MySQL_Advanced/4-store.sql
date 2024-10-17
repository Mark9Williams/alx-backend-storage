-- Create a trigger that decreases the quantity of an item after adding a new order

DELIMITER $$  -- Change the delimiter to allow for multi-line statements

CREATE TRIGGER decrease_item_quantity
AFTER INSERT ON orders  -- Trigger will fire after an insert on the orders table
FOR EACH ROW
BEGIN
    -- Update the quantity of the item in the items table
    UPDATE items
    SET quantity = quantity - NEW.quantity  -- Subtract the ordered quantity from the item's quantity
    WHERE id = NEW.item_id;  -- Reference the item using the item_id from the newly inserted order
END$$

DELIMITER ;  -- Reset the delimiter back to default
