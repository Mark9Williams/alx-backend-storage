-- Select the origin (country) and total number of fans (nb_fans) for each country

-- Group by the origin and order by the total number of fans in descending order
SELECT
    origin,
    SUM(nb_fans) AS nb_fans
FROM
    metal_bands
GROUP BY 
    origin
ORDER BY
    nb_fans DESC;
