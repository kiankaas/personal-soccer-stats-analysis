--NOTE: BigQuery is designed around the concept of immutable data structures and 
-- does not support the ALTER TABLE operation, thus I will have to create new tables
-- in order to add/remove columns to existing tables

# First remove all records of games where I did not play in. 
CREATE OR REPLACE TABLE `my-soccer-stats-439022.SoccerStats.temp_stats` AS
SELECT 
  Opponent, Goals, Assists, Goals_Forward, Goals_Against, 
  Match_Result, Season, Competition, date, Weather, Temperature
FROM `my-soccer-stats-439022.SoccerStats.raw_stats`
WHERE Goals IS NULL OR Goals IN ('1', '2', '3');
# for some reason (WHERE Goals != 'DNP') doesn't work, must be a BigQuery thing

# Next, group Weather conditions into 4 categories: Rain, Cloudy, Sunny, Brisk
-- NOTE: UPDATE statements in BigQuery requires there to be a WHERE clause 
UPDATE `my-soccer-stats-439022.SoccerStats.temp_stats`
SET Weather = CASE
  WHEN Weather LIKE '%Rain%' THEN 'Rain'
  WHEN Weather LIKE 'Overcast' THEN 'Cloudy'
  WHEN Weather LIKE 'Partially cloudy' AND Temperature BETWEEN 10 and 15 THEN 'Cloudy'
  WHEN Weather LIKE 'Clear' AND Temperature > 15 THEN 'Sunny'
  WHEN Weather LIKE 'Partially cloudy' AND Temperature > 15 THEN 'Sunny'
  WHEN Weather LIKE 'Clear' AND Temperature <= 15 THEN 'Brisk'
  WHEN Weather LIKE 'Partially cloudy' AND Temperature < 10 THEN 'Brisk'
  ELSE Weather
END
WHERE Weather LIKE '%Rain%' 
  OR Weather LIKE 'Overcast'
  OR Weather LIKE 'Partially cloudy' 
  OR Weather LIKE 'Clear';

# Next, replace all NULL values with 0, change the Goals and Assists columns 
# to INT64 data types, and add a "month" column
CREATE OR REPLACE TABLE `my-soccer-stats-439022.SoccerStats.cleaned_stats` AS
SELECT 
  Opponent, 
  IFNULL(CAST(Goals AS INT64), 0) AS Goals,  -- Cast Goals to INT64, then replace NULL with 0
  IFNULL(CAST(Assists AS INT64), 0) AS Assists,  -- Cast Assists to INT64, then replace NULL with 0
  Goals_Forward, 
  Goals_Against, 
  Match_Result, 
  Season, 
  Competition, 
  Date,
  CASE EXTRACT(MONTH FROM date) 
    WHEN 1 THEN 'JAN'
    WHEN 2 THEN 'FEB'
    WHEN 3 THEN 'MAR'
    WHEN 4 THEN 'APR'
    WHEN 5 THEN 'MAY'
    WHEN 6 THEN 'JUN'
    WHEN 7 THEN 'JUL'
    WHEN 8 THEN 'AUG'
    WHEN 9 THEN 'SEP'
    WHEN 10 THEN 'OCT'
    WHEN 11 THEN 'NOV'
    WHEN 12 THEN 'DEC'
  END AS Month,
  Weather, Temperature
FROM `my-soccer-stats-439022.SoccerStats.temp_stats`
ORDER BY Date;

# After running, these queries, can delete the temp_stats table in BigQuery
