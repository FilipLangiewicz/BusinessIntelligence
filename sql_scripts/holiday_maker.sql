-- Œwiêta sta³e
UPDATE dbo.Dim_Date SET IsHoliday = 1, HolidayText = 'Nowy Rok'
WHERE MONTH([date]) = 1 AND DAY([date]) = 1;

UPDATE dbo.Dim_Date SET IsHoliday = 1, HolidayText = 'Œwiêto Trzech Króli'
WHERE MONTH([date]) = 1 AND DAY([date]) = 6;

UPDATE dbo.Dim_Date SET IsHoliday = 1, HolidayText = 'Œwiêto Pracy'
WHERE MONTH([date]) = 5 AND DAY([date]) = 1;

UPDATE dbo.Dim_Date SET IsHoliday = 1, HolidayText = 'Œwiêto Konstytucji 3 Maja'
WHERE MONTH([date]) = 5 AND DAY([date]) = 3;

UPDATE dbo.Dim_Date SET IsHoliday = 1, HolidayText = 'Wniebowziêcie NMP'
WHERE MONTH([date]) = 8 AND DAY([date]) = 15;

UPDATE dbo.Dim_Date SET IsHoliday = 1, HolidayText = 'Wszystkich Œwiêtych'
WHERE MONTH([date]) = 11 AND DAY([date]) = 1;

UPDATE dbo.Dim_Date SET IsHoliday = 1, HolidayText = 'Œwiêto Niepodleg³oœci'
WHERE MONTH([date]) = 11 AND DAY([date]) = 11;

UPDATE dbo.Dim_Date SET IsHoliday = 1, HolidayText = 'Bo¿e Narodzenie'
WHERE MONTH([date]) = 12 AND DAY([date]) = 25;

UPDATE dbo.Dim_Date SET IsHoliday = 1, HolidayText = 'Drugi dzieñ Œwi¹t Bo¿ego Narodzenia'
WHERE MONTH([date]) = 12 AND DAY([date]) = 26;

-- Œwiêta ruchome: Wielkanoc, Poniedzia³ek Wielkanocny, Zielone Œwi¹tki, Bo¿e Cia³o
DECLARE @year INT = 1990;

WHILE @year <= 2030
BEGIN
    DECLARE @a INT = @year % 19;
    DECLARE @b INT = @year / 100;
    DECLARE @c INT = @year % 100;
    DECLARE @d INT = @b / 4;
    DECLARE @e INT = @b % 4;
    DECLARE @f INT = (@b + 8) / 25;
    DECLARE @g INT = (@b - @f + 1) / 3;
    DECLARE @h INT = (19 * @a + @b - @d - @g + 15) % 30;
    DECLARE @i INT = @c / 4;
    DECLARE @k INT = @c % 4;
    DECLARE @l INT = (32 + 2 * @e + 2 * @i - @h - @k) % 7;
    DECLARE @m INT = (@a + 11 * @h + 22 * @l) / 451;
    DECLARE @month INT = (@h + @l - 7 * @m + 114) / 31;
    DECLARE @day INT = ((@h + @l - 7 * @m + 114) % 31) + 1;

    DECLARE @easter DATE = DATEFROMPARTS(@year, @month, @day);
    DECLARE @easterMonday DATE = DATEADD(DAY, 1, @easter);
    DECLARE @pentecost DATE = DATEADD(DAY, 49, @easter);
    DECLARE @corpusChristi DATE = DATEADD(DAY, 60, @easter);

    UPDATE dbo.Dim_Date SET IsHoliday = 1, HolidayText = 'Wielkanoc'
    WHERE [date] = @easter;

    UPDATE dbo.Dim_Date SET IsHoliday = 1, HolidayText = 'Poniedzia³ek Wielkanocny'
    WHERE [date] = @easterMonday;

    UPDATE dbo.Dim_Date SET IsHoliday = 1, HolidayText = 'Zielone Œwi¹tki'
    WHERE [date] = @pentecost;

    UPDATE dbo.Dim_Date SET IsHoliday = 1, HolidayText = 'Bo¿e Cia³o'
    WHERE [date] = @corpusChristi;

    SET @year += 1;
END;

-- Ustaw wartoœci domyœlne tam, gdzie brak œwiêta
UPDATE dbo.Dim_Date
SET IsHoliday = 0
WHERE IsHoliday IS NULL;

UPDATE dbo.Dim_Date
SET HolidayText = ''
WHERE HolidayText IS NULL;
