# Personal Soccer Stats Analysis

## Background
My team competes in two leagues each year: the Burnaby Mens Soccer League (BMSL) during the Fall, and the Knight Soccer League (KSL) during the Summer. The Fall season runs from September-March, and the Summer season runs from April-August. Both leagues are divided into skill-based divisions, with Division 1 (D1) being the highest level of competition, followed by Division 2 (D2) and Division 3 (D3) respectively. In addition to the regular league matches, friendly games are also arranged throughout the year, typically between seasons. The BMSL also hosts a tournament-style cup every season, adding an extra competitive edge to the year. Although I only track basic stats, as I don't have access to my own advanced data/statistics, this project allows me to apply data analysis techniques to explore my performance across different seasons and leagues, even with a smaller dataset.

## The Data 
**Raw Data**: [raw_stats.csv](https://github.com/kiankaas/my-soccer-stats/blob/main/raw_stats.csv) <br/>
CHANGE TRACKING 

I've been manually tracking my soccer stats in a Google Sheets file. This file contains a comprehensive record of every game my team has played, spanning 105 records across 9 columns. Each record represents a game, capturing key statistics like goals, assists, and match outcomes, among other details as shown below:

| Variable   | Data Type | Description | 
|-------------|-------------|--------------|
| Opponent | string | The name of the opposing team in the match |
| Goals      | string| Number of goals I scored during the match  |
| Assists      | string      | Number of assists I made during the match | 
| Goals_Forward      | integer      | Number of goals my team scored during the match |
| Goals_Against      | integer      | Number of goals my team conceded during the match |
| Match_Result      | string      | The outcome of the match - indicating a win, loss, or draw| 
| Season      | string      | The soccer season in which the match was played in|
| Competition      | string      | The competition in which the match was part of |
| Date      | date      | The date the match took place |

### Enhancing the Data - Historical Weather APIs
To increase the dimensionality of the dataset and explore more factors influencing game outcomes, I added two new columns: **Weather** and **Temperature**. These additions allowed me to analyze how environmental conditions might impact match performances and outcomes. These columns are described below:

| Variable   | Data Type | Description | 
|-------------|-------------|--------------|
| Weather | string | The weather conditions during the match |
| Temperature      | integer| The temperature in degrees Celsius during the match  |

The weather data was retrieved using the [**Visual Crossing API**](https://www.visualcrossing.com/), which allowed me to match historical weather conditions and temperatures to each game based on the **Date** column in the dataset. Since I didn’t have specific timestamps for when each game occurred, I chose to pull the weather data for 6:00 PM each day, as our games typically take place in the evening, making this a reasonable average time to reflect game conditions.

I wrote a [Python script](https://github.com/kiankaas/my-soccer-stats/blob/main/GetWeather.py) to automate the process of querying the API for weather conditions and temperature at 6:00 PM on the day of each match. The script then updated the dataset with the retrieved weather information, ensuring that both the **Weather** and **Temperature** columns were accurately populated for each record.

This enhancement provides valuable context for analyzing the impact of external factors, such as weather conditions, on match outcomes and player performance. With these additions, I arrived at my final raw dataset, which is now ready for deeper exploration and analysis.

### Data Exploration
**SQL Query**: [Data Exploration](https://github.com/kiankaas/my-soccer-stats/blob/main/01-data-exploration.sql) <br/>
Before diving into the analysis, it is essential to prepare the dataset by exploring its structure, identifying any inconsistencies, and transforming the data as needed for a better analysis. I began by uploading the dataset as a table in **BigQuery**, which allows efficient querying and data exploration. In this stage, I explored the data structure, checked for missing values, ensured consistency in data formats, and converted categorical variables into usable formats where necessary.

After running some initial queries, here are my key observations:

1. There are **5** possible outcomes for **Match_Result**: D (draw), L (loss), W (win), PKL (loss via penalty shoot-out), and PKW (win via penalty shoot-out).
2. I've played in **3 Fall seasons** and **3 Summer seasons**: Fall 21/22, 22/23, 23/24 and Sum 22, 23, 24.
3. I've participated in **5 competitions**: BMSL D3, BMSL D2, BMSL Cup, KSL D2, and Friendlies.
4. The **Min** and **Max** values for **Goals_Forward** and **Goals_Against** are 0, 9, 0, and 7 respectively. No errors here.
5. Both the **Goals** and **Assists** columns are stored as string data types because games I didn't play in are marked as 'DNP' (Did Not Play). NULL values in these columns indicate 0 goals/assists in the game.
6. My team has faced a total of 47 different **opponents**. All opponents are named consistently.
7. The **date** column is in dd-mm-yyyy format, which was converted to a date type in BigQuery.
8. The **Weather** column has 7 possible values: "**Partially cloudy**", "**Overcast**", "**Clear**", "**Overcast, Rain**", "**Rain, Partially Cloudy**", "**Rain**", and "**Snow, Rain, Overcast**". 
9. The **Min** and **Max** values of the **Temperature** column are -1 and 26 respectively. No errors here.
10. There are **no outliers** in the dataset. 

### Data Cleaning/Transformation
**SQL Query**: [Data Cleaning](https://github.com/kiankaas/my-soccer-stats/blob/main/02-data-cleaning.sql) <br/>
**Cleaned data**: [cleaned_stats.csv](https://github.com/kiankaas/my-soccer-stats/blob/main/cleaned_stats.csv) <br/>

To clean and prepare the data for analysis, I made the following transformations:

1. Removed records for games I **did not play**.
2. Added a "**Month**" column to facilitate monthly trend analysis.
3. Replaced all **NULL** values with 0.
4. Grouped **Weather** conditions into 4 categories for simplicity:
     - **Rain**: Includes any conditions that mention "Rain".
     - **Cloudy**: Includes "Partially cloudy" conditions on cooler days (10°C <= Temperature <= 15°C) , and all "Overcast" conditions.
     - **Sunny**: Includes "Clear" and "Partially cloudy" conditions on warmer days (Temperature > 15°C).
     - **Brisk**: Used for colder, clear days, including "Clear" conditions with Temperature < 15°C, and "Partially cloudy" conditions with Temperature < 10°C. 
5. Converted the **Goals**, **Assists**, and **Goals+Assists** columns to **integer** data types.

With these changes, our dataset is now organized, consistent, and ready for analysis.

### Data Encoding
**Python Script**: [link]() <br/>
To ensure meaningful analysis, categorical variables were **numerically encoded**, allowing for **correlation analysis** and structured comparisons across different conditions. The endcoding
choices were carefully designed to maintain logical consistency - **higher values indicate more challenging conditions** across all categories.  

**Competition Level** 
| Competition   | Encoded Value | Description | 
|-------------|-------------|--------------|
| Friendly | 1 | Least competitive (exhibition matches) |
| BMSL D3      | 2| Division 3, lowest league division  |
| BMSL Cup      | 3      | Knockout tournament with mixed opponent strength | 
| BMSL D2      | 4      | Division 2, higher level of competition |
| KSL D2      | 5      | Most competitive league (summer league with stronger teams) |

Competitions were assigned numerical values to allow for structured comparisons in performance across different leagues.

**Season Difficulty** 
| Season   | Encoded Value | Competitions Played (games played) | 
|-------------|-------------|--------------|
| Fall 21/22 | 1.95 | BMSL D3 (14), BMSL Cup (2), Friendly (3) |
| Sum 22      | 4.56 | KSL D2 (8), Friendly (1)  |
| Fall 22/23      | 3.80      | BMSL D2 (12), BMSL Cup (3) | 
| Sum 23      | 3.77      | KSL D2 (9), Friendly (4) |
| Fall 23/24      | 3.76      | BMSL D2 (18), BMSL Cup (2), Friendly (1) |
| Sum 24      | 5.00      | KSL D2 (5) |

To reflect the overall competition difficulty for each season, a **weighted average competition score** was computed using the formula:
**Season Score** = ( Σ (Games in Competition × Competition Score) ) ÷ ( Σ Total Games in Season )

**Match Result** 
| Match Result   | Encoded Value | Description | 
|-------------|-------------|--------------|
| L | 3 | Loss |
| PKL      | 2 | Loss via penalty shoot-out  |
| D      | 1      | Draw | 
| PKW      | 1      | Win via penalty shoot-out |
| W      | 0      | Win |

Match results were encoded based on the league's point system, where teams earn 3 points for a win, 2 for a win via penalty shoot-out, 1 for a draw or a loss via penalty shoot-out, and 0 for a loss — but reversed so that higher values indicate more difficult outcomes.
This encoding maintains consistency with real-world soccer scoring while ensuring that increasing values across all encoded variables represent greater difficulty.

**Weather Conditions**
| Weather COndition   | Encoded Value | Description | 
|-------------|-------------|--------------|
| Sunny      | 1 | Best conditions |
| Cloudy      | 2 | Mild but playble  |
| Brisk      | 2.5      | Colder but manageable | 
| Rain      | 3      | Most difficult (wet field, low visibility) |

Weather conditions were encoded to analyze performance trends in different environments, considering factors like temperature, visibility, and field conditions.

## Analysis
**SQL Query**: [link]() <br/>

### Correlation Matrix Analysis

To gain deeper insights into performance trends and influencing factors, I generated a **correlation matrix** using Pearson correlation coefficients. This statistical method measures the strength and direction of the linear relationship between two variables, with values ranging from:

- **+1**: Strong positive correlation (both variables increase together)
- **0**: No correlation (no linear relationship) 
- **-1**: Strong negative correlation (one variable increases while the other decreases)
     
By examining correlations between match performance factors, I aimed to identify key trends and relationships that impact results.
The following columns were **not included** in the correlation matrix: **Date**, **Opponent**, **Month**, and **Temperature**. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/4cdde0b0-e00b-445e-83fc-881e3e4a53c0" alt="correlation-matrix" width="750">
</p>

#### Expected Findings 
- **Goals and Goal Contributions have a strong positive correlation (0.88)**
     - My offensive impact is more weighted towards scoring goals rather than assisting goals.
     - As a striker, I rely more on finishing chances than creating them. 
- **Goals Forward and Goal Contributions have a strong positive correlation (0.72)**
     - When my team scores, I am usually involved - either by scoring or assisting.
     - Since joining the team, I have consistently been the top scorer, even winning BMSL's D2 Golden Boot award in Fall 23/24.    
- **Goals Forward and Match Result have a moderate negative correlation (-0.58)**
     - More goals scored by the team directly lead to better match results. 
     - This confirms that attacking success is a strong predictor of winning. 
- **Goals Against and Match Result have a strong positive correlation (0.68)**
     - The more goals the team concedes, the worse the match result is likely to be. 
     - This confirms that defensive stability plays a key role in match success. 
- **Season and Competition have a strong positive correlation (0.70)**
     - Over time, my team has played in more difficult leagues.
     - After being promoted to BMSL D2, we have continued playing at a higher competition level. 

#### Surprising Observations
- **Competition has a weak negative correlation with both Goals and Goal_Contributions (-0.19 and -0.18)**
     - My goals and goal contributions remained steady across all competitions but dropped significantly in KSL D2. 
     - This suggests that the increase in opponent skill level in KSL D2 is a bigger jump compared to other leagues.
- **Match Result and Goal Contributions have a moderate negative correlation (-0.38)**
     - While I expected my goal contributions to strongly determine match success, the correlation is weaker than anticipated.
     - This suggests that other factors — such as overall team attacking play and defensive performance — play a significant role in match outcomes. 
- **Weather and Match Result have a weak negative correlation (-0.20)** 
     - My team’s performance remained relatively stable across different weather conditions.  
     - However, further analysis revealed that win percentage is actually lowest in sunny conditions and highest in brisk/rainy conditions. 
     - A possible explanation is that most KSL D2 matches were played in sunny weather, which overlaps with our team’s weakest performances. 
- **Weather has almost no correlation with Goals, Assists, and Goal Contributions (0.02, 0.01, and 0.02)** 
     - My personal performance remains consistent regardless of weather conditions. 
     - External factors such as rain or cold temperatures do not appear to strongly impact my ability to score or assist. 

#### Interesting Patterns
- **Weather and Goals Against have a weak to moderate negative correlation (-0.28)** 
     - Interestingly, my team concedes fewer goals in poor weather conditions. 
     - While rain speeds up the ball on turf, it may also lead to more defensive clearances, scrappy play, and fewer structured attacking opportunities for opponents. 
- **Competition and Match Result have a weak positive correlation (0.25)** 
     - Despite facing stronger opponents, my team’s win percentage remained relatively stable — except in KSL D2, where it dropped significantly. 
     - This suggests that while the team adapted well to tougher leagues, KSL D2 presented a much larger challenge, both individually and as a team. 
- **Goals Forward and Goals Against have a weak negative correlation (-0.14)**
     - When my team scores more, we don't necessarily concede fewer goals.
     - This may indicate that my team doesn't rely on defensive stability and shutting down the opponent to win games, but rather by outscoring the opponent.
 
## Deeper Analysis with Visualizations

This section expands on key correlations by using visualizations to better understand the relationships between team performance and individual performance. The goal is to analyze what factors impact performance on both levels, identifying patterns that influence match outcomes (team success) and personal contributions (goals & assists).

This section expands on key observations by using visualizations to better understand the relationship between external factors and match performance. The analysis is split into two main sections: Team Performance Analysis and Individual Performance Analysis.

## Team Performance Analysis

### 1. Win Percentage by Competition & Weather

**Win Percentage by Competition Level** 

**Key Insight**: My team's win percentage remained stable across most competitions (64-72%), but dropped significantly in KSL D2 (32%).

**Possible Explanations**:

- **Stronger Opposition**: KSL D2 features more competitive teams, making it harder to win matches.  
- **Decline in Team Scoring Output**: The correlation matrix shows a **negative correlation between Goals Forward and Competition (-0.29)**, indicating that as competition level increases, the number of goals scored per game decreases. This suggests that tougher leagues limit offensive opportunities. 
     
<p align="center">
  <img src="https://github.com/user-attachments/assets/93b68f8c-587c-4083-b0c9-6128d36586ab" alt="win%-comp" width="500"> 
</p>

**Offensive & Defensive Performance by Competition**

**Key Insight**: My team's attacking output (1.64 goals forward per game) and defensive stability (2.91 goals against per game) are at their worst in KSL D2. 

**Possible Explanation**:

- **More Defensive Opponents**: Stronger defenses in KSL D2 limit scoring chances, contributing to the lowest Goals Forward per game. 
- **Tougher Opposition in Attack**: KSL D2 features stronger attacking teams, leading to the highest Goals Against per game.
- **Overall Competitive Challenge**: The combined effects of tougher defenses and stronger opposition in attack result in both a lower scoring output and higher goals conceded in KSL D2.

<p align="center">
  <img src="https://github.com/user-attachments/assets/cee5f7c0-1b29-4243-9894-1e57a9a19a1b" alt="goals-against-comp" width="500">   <img src="https://github.com/user-attachments/assets/d5e2dad5-a982-4f94-9a2f-b701bfdb5bf9" alt="goals-forward-comp" width="500"> 
</p>

**Win Percentage & Weather Impact** 

**Key Insight**: My team’s win percentage was lowest in sunny conditions (37.5%) and highest in rainy conditions (68.2%). 

**Possible Explanations**:

- **Competition Overlaps with Weather**: Many KSL D2 matches took place in sunny conditions, which could indicate that competition level played a bigger role in performance than weather itself. 
- **Opponent Playstyle Disruption**: Poor weather conditions may impact opponent playstyles more than ours, leading to higher success rates.
- **Stable Attacking Output**: Despite defensive struggles in poor weather, Goals Forward per game remains relatively consistent, suggesting that my team’s offensive performance is not significantly affected by weather.


<p align="center">
  <img src="https://github.com/user-attachments/assets/dded4263-f369-4ce8-bfee-610118c83f78" alt="win%-weather" width="500"> <img src="https://github.com/user-attachments/assets/ba3cfafb-393b-4f2d-8fb2-8ebb74bc6bef" alt="KSL-win%weather" width="500">
     <img src="https://github.com/user-attachments/assets/b4c6d3d9-1849-4be5-a297-b37393d145f0" alt="goals-forward-weather" width="500">
</p>


### 2. Weather & Match Results

**Offensive & Defensive Performance by Weather Condition**

**Key Insight**: My team conceded the most goals in sunny conditions (3.00 per game), while scoring output remained stable across all weather conditions. 

**Possible Explanations**: 

- **Defensive Instability in Sunny Conditions**: The increase in goals conceded in sunny conditions suggests that defensive struggles, rather than offensive inefficiencies, are the primary reason for lower win rates.  
- **Consistent Attacking Performance**: The consistency in goals forward across all weather conditions indicates that attacking performance was unaffected by weather, while defense was more vulnerable. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/a5157b3b-2f32-4d71-b970-a265cbfae102" alt="win%-comp" width="500">  <img src="https://github.com/user-attachments/assets/013fcb5e-9141-44e1-907c-17e028771c4d" alt="win%-comp" width="500">  
</p>

### 3. Goals Conceded by Weather Condition & Competition Level 

**Key Insight**: The number of goals my team concedes in sunny conditions is highest in KSL D2 (4.14 per game), reinforcing that the competition level is the strongest factor in performance.

**Possible Explanation**:

- **Higher Goals Against in KSL D2**: Even in non-sunny conditions, KSL D2 consistently records some of the highest goals-against rates, accounting for three of the four highest goals conceded per game across and competition and weather combinations.
- **Sunny Weather Coinciding with Difficult Matches**: While my team conceded more goals in sunny weather, it is likely due to stronger opponents rather than the weather itself.

<p align="center">
  <img src="https://github.com/user-attachments/assets/308d86c3-4916-44fe-a8f6-80606b3f250f" alt="win%-comp" width="750"> 
</p>




# BREAK 






**Goals Conceded by Weather Condition & Competition Level** 
- **Key Insight**: The number of goals my team concedes in sunny conditions is highest in KSL D2 (4.14 per game), reinforcing that the competition level is the strongest factor in performance.

- **Possible Explanation**:
     - Even in non-sunny conditions, KSL D2 consistently records some of the highest goals-against rates, accounting for three of the four highest goals conceded per game across and competition and weather combinations.
     - Sunny conditions in KSL D2 correlate with the most goals conceded, but this is likely due to stronger opposition rather than the weather itself.

<p align="center">
  <img src="https://github.com/user-attachments/assets/308d86c3-4916-44fe-a8f6-80606b3f250f" alt="win%-comp" width="750"> 
</p>





### Weather & Match Results






**Win Percentage in KSL D2 by Weather Condition**
- **Key Insight**: My team never won a match in KSL D2 under sunny conditions (7 games played, 7 loses).

- **Possible Explanation**:
     - KSL D2 performance was weakest in sunny conditions, suggesting that the competition level, not weather, is the primary factor affecting match results.
     - The moderate win rates in rain and cloudy conditions indicate that while weather may play a role, it does not fully explain performance trends.
 
<p align="center">
  <img src="https://github.com/user-attachments/assets/ba3cfafb-393b-4f2d-8fb2-8ebb74bc6bef" alt="win%-comp" width="500"> 
</p>






Create a project goal section at top (find what impacts my individual performance and team performance.

Individual section? Team section? Or combine both?


graph: win percentage in games I've scored or assisted in vs games I didn't score or assist in. 








**Correlation vs. Causation**  
The correlation suggests stronger opponents are more difficult to outscore, but other factors could also contribute, such as: 

**1. Lack of Weekly Practices**
- During the Fall league season, our team practices once a week, helping maintain fitness and tactical awareness.
- During the Summer league season, there are no weekly practices, which may lead to rusty play and fatigue over time.

**2. Missing Key Players** 
- The Summer season overlaps with vacation time, resulting in frequent absences of key players throughout the season.
- This disrupts team chemistry and forces adjustments to the lineup more often than in the Fall season.

**3. Frequent Roster Changes and Player Tryouts**
- The KSL summer league allows new players to register at any time during the season.
- As a result, our team frequently brings in new players for tryouts, making it difficult to build chemistry with teammates.

**4. Increased Game Intensity in KSL D2**
- Stronger defenses in KSL D2 may allow fewer attacking chances.
- The pace and physicality of the league make it harder to maintain possession and create goal-scoring opportunities.





