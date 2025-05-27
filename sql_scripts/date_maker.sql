WITH DateSequence AS (
    SELECT CAST('19900101' AS DATE) AS [Date]
    UNION ALL
    SELECT DATEADD(DAY, 1, [Date])
    FROM DateSequence
    WHERE [Date] < '20301231'
),
DateData AS (
    SELECT
        d.[Date],
        DAY(d.[Date]) AS [Day],
        CASE 
            WHEN DAY(d.[Date]) IN (11,12,13) THEN 'th'
            WHEN RIGHT(CAST(DAY(d.[Date]) AS VARCHAR(2)),1) = '1' THEN 'st'
            WHEN RIGHT(CAST(DAY(d.[Date]) AS VARCHAR(2)),1) = '2' THEN 'nd'
            WHEN RIGHT(CAST(DAY(d.[Date]) AS VARCHAR(2)),1) = '3' THEN 'rd'
            ELSE 'th'
        END AS [DaySuffix],
        DATEPART(WEEKDAY, d.[Date]) AS [Weekday],
        DATENAME(WEEKDAY, d.[Date]) AS [WeekDayName],
        CASE WHEN DATENAME(WEEKDAY, d.[Date]) IN ('Saturday', 'Sunday') THEN 1 ELSE 0 END AS [IsWeekend],
        NULL AS [IsHoliday],
        (DAY(d.[Date]) - 1) / 7 + 1 AS [DOWInMonth],
        DATEPART(DAYOFYEAR, d.[Date]) AS [DayOfYear],
        DATEPART(WK, d.[Date]) - DATEPART(WK, DATEADD(DAY, 1 - DAY(d.[Date]), d.[Date])) + 1 AS [WeekOfMonth],
        DATEPART(WK, d.[Date]) AS [WeekOfYear],
        DATEPART(ISO_WEEK, d.[Date]) AS [ISOWeekOfYear],
        MONTH(d.[Date]) AS [Month],
        DATENAME(MONTH, d.[Date]) AS [MonthName],
        DATEPART(QUARTER, d.[Date]) AS [Quarter],
        'Q' + CAST(DATEPART(QUARTER, d.[Date]) AS VARCHAR(1)) AS [QuarterName],
        YEAR(d.[Date]) AS [Year],
        RIGHT('0' + CAST(MONTH(d.[Date]) AS VARCHAR(2)), 2) + CAST(YEAR(d.[Date]) AS CHAR(4)) AS [MMYYYY],
        LEFT(DATENAME(MONTH, d.[Date]), 3) + CAST(YEAR(d.[Date]) AS CHAR(4)) AS [MonthYear],
        DATEFROMPARTS(YEAR(d.[Date]), MONTH(d.[Date]), 1) AS [FirstDayOfMonth],
        EOMONTH(d.[Date]) AS [LastDayOfMonth],
        DATEADD(QUARTER, DATEDIFF(QUARTER, 0, d.[Date]), 0) AS [FirstDayOfQuarter],
        DATEADD(DAY, -1, DATEADD(QUARTER, DATEDIFF(QUARTER, 0, d.[Date]) + 1, 0)) AS [LastDayOfQuarter],
        DATEFROMPARTS(YEAR(d.[Date]), 1, 1) AS [FirstDayOfYear],
        DATEFROMPARTS(YEAR(d.[Date]), 12, 31) AS [LastDayOfYear],
        NULL AS [HolidayText]
    FROM DateSequence d
)
MERGE dbo.Dim_Date AS target
USING DateData AS source
    ON target.[date] = source.[Date]
WHEN MATCHED THEN
    UPDATE SET
        [Day] = source.[Day],
        [DaySuffix] = source.[DaySuffix],
        [Weekday] = source.[Weekday],
        [WeekDayName] = source.[WeekDayName],
        [IsWeekend] = source.[IsWeekend],
        [IsHoliday] = source.[IsHoliday],
        [DOWInMonth] = source.[DOWInMonth],
        [DayOfYear] = source.[DayOfYear],
        [WeekOfMonth] = source.[WeekOfMonth],
        [WeekOfYear] = source.[WeekOfYear],
        [ISOWeekOfYear] = source.[ISOWeekOfYear],
        [Month] = source.[Month],
        [MonthName] = source.[MonthName],
        [Quarter] = source.[Quarter],
        [QuarterName] = source.[QuarterName],
        [Year] = source.[Year],
        [MMYYYY] = source.[MMYYYY],
        [MonthYear] = source.[MonthYear],
        [FirstDayOfMonth] = source.[FirstDayOfMonth],
        [LastDayOfMonth] = source.[LastDayOfMonth],
        [FirstDayOfQuarter] = source.[FirstDayOfQuarter],
        [LastDayOfQuarter] = source.[LastDayOfQuarter],
        [FirstDayOfYear] = source.[FirstDayOfYear],
        [LastDayOfYear] = source.[LastDayOfYear],
        [HolidayText] = source.[HolidayText]
WHEN NOT MATCHED THEN
    INSERT (
        [date], [Day], [DaySuffix], [Weekday], [WeekDayName], [IsWeekend], [IsHoliday],
        [DOWInMonth], [DayOfYear], [WeekOfMonth], [WeekOfYear], [ISOWeekOfYear],
        [Month], [MonthName], [Quarter], [QuarterName], [Year], [MMYYYY], [MonthYear],
        [FirstDayOfMonth], [LastDayOfMonth], [FirstDayOfQuarter], [LastDayOfQuarter],
        [FirstDayOfYear], [LastDayOfYear], [HolidayText]
    )
    VALUES (
        source.[Date], source.[Day], source.[DaySuffix], source.[Weekday], source.[WeekDayName], source.[IsWeekend], source.[IsHoliday],
        source.[DOWInMonth], source.[DayOfYear], source.[WeekOfMonth], source.[WeekOfYear], source.[ISOWeekOfYear],
        source.[Month], source.[MonthName], source.[Quarter], source.[QuarterName], source.[Year], source.[MMYYYY], source.[MonthYear],
        source.[FirstDayOfMonth], source.[LastDayOfMonth], source.[FirstDayOfQuarter], source.[LastDayOfQuarter],
        source.[FirstDayOfYear], source.[LastDayOfYear], source.[HolidayText]
    )
OPTION (MAXRECURSION 0);
