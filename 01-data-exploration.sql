# Find all possible match outcomes
SELECT DISTINCT Match_Result
FROM `my-soccer-stats-439022.SoccerStats.raw_stats`;
-- there are 5 possible match outcomes: D, L, W, PKL, PKW 

# Find all seasons I've played a match in
SELECT DISTINCT Season
FROM `my-soccer-stats-439022.SoccerStats.raw_stats`;
-- I've played in 3 fall seasons and 3 summer seasons

# Find all competitions I've played a match in. 
SELECT DISTINCT Competition
FROM `my-soccer-stats-439022.SoccerStats.raw_stats`;
-- I've participated in 5 competitions: BMSL D3, BMSL D2, BMSL Cup, KSL D2, and Friendlies

# Find min and max values for Goals_Forward and Goals_Against
SELECT MIN(Goals_Forward) as min_gf, MAX(Goals_Forward) as max_gf, 
MIN(Goals_Against) as min_ga, MAX(Goals_Against) as max_ga
FROM `my-soccer-stats-439022.SoccerStats.raw_stats`;
-- 0, 9, 0, 7 respectively

# Inspect all values in Goals column
SELECT DISTINCT Goals
FROM `my-soccer-stats-439022.SoccerStats.raw_stats`;
-- 5 different values for Goals: null, 1, 2, 3, DNP

# Inspect all values in Assists column
SELECT DISTINCT Assists
FROM `my-soccer-stats-439022.SoccerStats.raw_stats`;
-- 4 different revaluessults for Goals: null, 1, 2, DNP

# Check for any errors in Opponent name
SELECT Opponent, Count(*) as games_played
FROM `my-soccer-stats-439022.SoccerStats.raw_stats`
GROUP BY Opponent
ORDER BY games_played DESC;
-- No errors, all teams named consistently

# Check for all possible Weather conditions
SELECT DISTINCT Weather, COUNT(*)
FROM `my-soccer-stats-439022.SoccerStats.raw_stats`
GROUP BY Weather;
-- There are 7 possible values for Weather

# Find min and max values for Temperature
SELECT MIN(Temperature) as min_temp, MAX(Temperature) as max_temp
FROM `my-soccer-stats-439022.SoccerStats.raw_stats`;
-- min_temp = -1, max_temp = 26





