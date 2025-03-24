# Data Cleaning: 
-- 
-- Replace all NULL and 'DNP' values with 0
-- Change the Goals and Assists columns to INT64 data types
-- Add Goal_Contributions, Competition_Level, and Played columns
-- Group Weather conditions into 4 categories: Rain, Cloudy, Sunny, Brisk

CREATE OR REPLACE TABLE `my-soccer-stats-439022.SoccerStats.cleaned_stats` AS
SELECT 
  Opponent, 
  
  -- Standardize 'DNP' and missing values to 0 and cast as integers
  SAFE_CAST(IF(LOWER(Goals) IN ('dnp', '') OR Goals IS NULL, '0', Goals) AS INT64) AS Goals,
  SAFE_CAST(IF(LOWER(Assists) IN ('dnp', '') OR Assists IS NULL, '0', Assists) AS INT64) AS Assists,
  
  -- Goal Contributions column
  IFNULL(SAFE_CAST(Goals AS INT64), 0) + IFNULL(SAFE_CAST(Assists AS INT64), 0) AS Goal_Contributions,

  Goals_Forward, 
  Goals_Against, 
  Match_Result, 
  Season, 
  Competition, 

  -- Competition Level Mapping
  CASE Competition
    WHEN 'KSL D2' THEN 5
    WHEN 'BMSL D2' THEN 4
    WHEN 'BMSL Cup' THEN 3
    WHEN 'BMSL D3' THEN 2
    WHEN 'Friendly' THEN 1
    ELSE NULL
  END AS Competition_Level,

  Date,

  -- Played Column to track games I played in
  IF(LOWER(Goals) = 'dnp' OR LOWER(Assists) = 'dnp', 'No', 'Yes') AS Played,

  -- Group Weather Conditions
  CASE 
    WHEN Weather LIKE '%Rain%' THEN 'Rain'
    WHEN Weather LIKE 'Overcast' THEN 'Cloudy'
    WHEN Weather LIKE 'Partially cloudy' AND Temperature BETWEEN 10 and 15 THEN 'Cloudy'
    WHEN Weather LIKE 'Clear' AND Temperature > 15 THEN 'Sunny'
    WHEN Weather LIKE 'Partially cloudy' AND Temperature > 15 THEN 'Sunny'
    WHEN Weather LIKE 'Clear' AND Temperature <= 15 THEN 'Brisk'
    WHEN Weather LIKE 'Partially cloudy' AND Temperature < 10 THEN 'Brisk'
    ELSE Weather
  END AS Weather,

  Temperature

FROM `my-soccer-stats-439022.SoccerStats.raw_stats`
ORDER BY Date;
