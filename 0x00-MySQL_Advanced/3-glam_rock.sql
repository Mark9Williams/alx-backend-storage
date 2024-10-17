-- Create a script to list all bands with Glam rock as their main style, ranked by longevity

-- Use a common table expression (CTE) to calculate lifespan for clarity
SELECT
    band_name,
    COALESCE(split, 2022) - formed AS lifespan
FROM
    metal_bands
WHERE
    style LIKE '%Glam rock%'
ORDER BY
    lifespan DESC;
