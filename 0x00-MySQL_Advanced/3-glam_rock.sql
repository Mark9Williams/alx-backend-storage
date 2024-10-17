-- a SQL script that lists all bands with Glam rock as their main style, ranked by their longevity

-- Creating a common table expression (CTE) called glam_rock_bands
WITH glam_rock_bands AS (
    SELECT
        band_name,
        COALESCE(split, 20222) - formed AS lifespan
    FROM
        metal_bands
    WHERE
        style LIKe '%Glam rock%'
)

-- Selecting the name and lifespan of the bands from the CTE, ordering by lifespan in descending order
SELECT
    band_name,
    lifespan
FROM
    glam_rock_bands
ORDER BY
    lifespan DESC;
