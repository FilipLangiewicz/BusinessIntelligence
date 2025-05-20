-- Upewnij siê, ¿e tabela Dim_Date ma kolumnê date_id typu DATE
-- CREATE TABLE dbo.Dim_Date (
--     date_id DATE PRIMARY KEY
-- );

WITH Dates AS (
    SELECT CAST('1990-01-01' AS DATE) AS date_value
    UNION ALL
    SELECT DATEADD(DAY, 1, date_value)
    FROM Dates
    WHERE date_value < '2030-12-31'
)
INSERT INTO dbo.Dim_Date (date_id)
SELECT date_value
FROM Dates
OPTION (MAXRECURSION 0);
