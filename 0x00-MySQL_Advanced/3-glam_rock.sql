-- Create a script to list all bands with Glam rock as their main style, ranked by longevity

-- Use a common table expression (CTE) to calculate lifespan for clarity
WITH band_lifespans AS (
    SELECT 
        band_name,
        COALESCE(split, 2022) - formed AS lifespan
    FROM 
        metal_bands
    WHERE 
        style LIKE '%Glam rock%'
)

-- Select the desired columns and order by lifespan in descending order
SELECT 
    band_name, 
    lifespan
FROM 
    band_lifespans
ORDER BY 
    lifespan DESC;
