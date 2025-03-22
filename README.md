# Personal Soccer Stats Analysis

## Introduction

This project analyzes my personal soccer performance and my team's results over three years using data I've manually collected. By combining key metrics with additional insights such as weather conditions and competition level, this project aims to uncover meaningful patterns and insights.

## Background

I have been a lifelong soccer player and fan, having played club soccer from the age of 5 until 18. After taking a three-year break from the sport, I returned to soccer in 2021 when I joined Fraser Mills FC United, a Burnaby-based amateur men's soccer club where I play as the team's striker.

My passion for both soccer and data inspired me to start recording my performances out of curiosity — I thought it would be interesting to see my own statistics. Over time, this evolved into a valuable tool for analyzing my contributions on the field and understanding my overall performance.

Without access to official data in my amateur leagues, I manually recorded key metrics such as goals, assists, and match outcomes to gain insights into both my individual performance and my team’s attacking output. This project combines my love for soccer with my interest in data analysis, allowing me to explore trends, patterns, and areas for growth.

<div align="center">
  <img src="https://github.com/user-attachments/assets/a170e12e-86f2-41f7-b462-3e5dc9239be7" alt="action-shot" width="500">
  <p style="text-align: center;"><em>Me in action during a Burnaby Men's Soccer League match.</em></p>
</div>

## Purpose 

The primary purpose of this project is to analyze both my personal soccer performance and my team's performance over my first three years with the club. By examining key metrics such as goals, assists, and match outcomes, this project aims to: 
- **Identify trends in my individual goal-scoring and contribution patterns** to assess how my performance has evolved over time.
- **Evaluate my team's overall attacking performance and goal distribution** to understand how our offensive and defensive output has varied across seasons.
- **Investigate factors such as weather conditions and competition level** to uncover potential influences on performance and consistency.

Understanding these patterns can provide valuable insights to improve my performance and inform my team’s tactical approach.

## The Data 
Raw Dataset: [raw_stats.csv](https://github.com/kiankaas/my-soccer-stats/blob/main/raw_stats.csv) <br/>

### Dataset Overview 

This dataset captures performance data from every game my team has played since I joined in 2021. Since no official tracking system was available for my amateur soccer leagues, I decided to take matters into my own hands. I began manually tracking my performance using Google Sheets, recording key statistics from every game my team played. This included goals scored, match outcomes, leagues, and more. While this method required additional effort, it allowed me to gain valuable insights into my performance and identify trends that may have otherwise gone unnoticed.

The dataset contains **105 records** across **9 key variables**, with each record representing one match. Although my dataset tracks only basic stats like goals and assists, it covers my first three years with the team, providing a meaningful foundation for analysis. The dataset structure is shown below:

<div align="center">

| Variable   | Data Type | Description | Example Value |
|-------------|-------------|--------------|--------------|
| Opponent | string | The name of the opposing team in the match | Hastings FC |
| Goals      | string| Number of goals I scored during the match  | 2 |
| Assists      | string      | Number of assists I made during the match | 1 |
| Goals_Forward      | integer      | Number of goals my team scored during the match | 3 |
| Goals_Against      | integer      | Number of goals my team conceded during the match | 1 |
| Match_Result      | string      | The outcome of the match - indicating a win, loss, or draw| W |
| Season      | string      | The soccer season in which the match was played in| Fall 23/24 |
| Competition      | string      | The competition in which the match was part of | BMSL D2 |
| Date      | date      | The date the match took place | 2023-10-15 |

</div>

### League & Competition Details

My team competes in two leagues each year: the **Burnaby Men's Soccer League (BMSL)** in the Fall (September to March) and the **Knight Soccer League (KSL)** in the Summer (April to August). Both leagues are divided into three skill-based divisions: **Division 1 (D1)** for top competition, **Division 2 (D2)** for intermediate competition, and **Division 3 (D3)** as the least competitive division. In addition to league matches, my dataset also includes **Friendly** games (typically played between seasons as exhibition) and **BMSL Cup** matches, a knockout-style tournament with varied opponent strength. 

These details provide important context for understanding the competition levels reflected in the data cleaning section later on.

### Enhancing the Data - Historical Weather APIs
To gain deeper insights into factors influencing match outcomes and performance, I expanded my dataset by incorporating **Weather** and **Temperature** data. These additions allowed me to analyze how environmental conditions may have impacted match performances and outcomes.
The following columns were added to the dataset:

<div align="center">

| Variable   | Data Type | Description | Example Value |
|-------------|-------------|--------------|--------------|
| Weather | string | The weather conditions during the match | Clear |
| Temperature      | integer| The temperature in degrees Celsius during the match  | 15 | 

</div>

The weather data was retrieved using the [**Visual Crossing API**](https://www.visualcrossing.com/), which allowed me to match historical weather conditions and temperatures to each game based on the **Date** column. Since I don’t have specific timestamps for when each game occurred, and my team's matches are typically played in the evening, I chose to retrieve weather data for **6:00 PM** on each game day to reflect match conditions as accurately as possible.

I wrote a [Python script](https://github.com/kiankaas/my-soccer-stats/blob/main/GetWeather.py) to automate the data retrieval process. The script efficiently queried the API for weather conditions and temperature, updating my dataset to ensure each record contained accurate environmental details. With this enhancement, my dataset now captures both on-field performance and external conditions, providing valuable context for deeper analysis.

### Data Exploration
SQL Query: [Data Exploration](https://github.com/kiankaas/my-soccer-stats/blob/main/01-data-exploration.sql) <br/>

Before diving into the analysis, it is essential to prepare the dataset by exploring its structure, identifying any inconsistencies, and transforming the data as needed for a better analysis. After running some initial queries, here are my key observations:

1. There are **5** possible outcomes for **Match_Result**: D (draw), L (loss), W (win), PKL (loss via penalty shoot-out), and PKW (win via penalty shoot-out).
2. The dataset includes **3 Fall seasons** and **3 Summer seasons**: Fall 21/22, 22/23, 23/24 and Sum 22, 23, 24.
3. Matches were played in the following **5 competitions**: BMSL D3, BMSL D2, BMSL Cup, KSL D2, and Friendlies.
4. The **Min** and **Max** values for **Goals_Forward** and **Goals_Against** are 0, 9, 0, and 7 respectively. No errors here.
5. Both the **Goals** and **Assists** columns are stored as string data types because games I didn't play in are marked as 'DNP' (Did Not Play). NULL values in these columns indicate 0 goals/assists in the game.
6. My team has faced a total of 47 different **opponents**. All opponents are named consistently.
7. The **date** column is in dd-mm-yyyy format, which was converted to a date type in BigQuery.
8. The **Weather** column has 7 possible values: "**Partially cloudy**", "**Overcast**", "**Clear**", "**Overcast, Rain**", "**Rain, Partially Cloudy**", "**Rain**", and "**Snow, Rain, Overcast**". 
9. The **Min** and **Max** values of the **Temperature** column are -1 and 26 respectively. No errors here.
10. There are **no outliers** in the dataset. 

### Data Cleaning
SQL Query: [Data Cleaning](https://github.com/kiankaas/my-soccer-stats/blob/main/02-data-cleaning.sql) <br/>
Cleaned Dataset: [cleaned_stats.csv](https://github.com/kiankaas/my-soccer-stats/blob/main/cleaned_stats.csv) <br/>

To clean and prepare the data for analysis, I made the following transformations:

1. Removed **'Did Not Play' (DNP)** records.
2. Replaced all **NULL** values with 0.
3. Grouped **Weather** conditions into 4 categories for simplicity:
     - **Rain**: Includes any conditions that mention "Rain".
     - **Cloudy**: Includes "Partially cloudy" conditions on cooler days (10°C <= Temperature <= 15°C) , and all "Overcast" conditions.
     - **Sunny**: Includes "Clear" and "Partially cloudy" conditions on warmer days (Temperature > 15°C).
     - **Brisk**: Used for colder, clear days, including "Clear" conditions with Temperature < 15°C, and "Partially cloudy" conditions with Temperature < 10°C. 
4. Created a **Goal_Contributions** column, which is a sum of **Goals** and **Assists**.
5. Converted the **Goals**, **Assists**, and **Goal_Contributions** columns to **integer** data types.
6. Added a **Competition_Level** column to enable performance comparisons across varying competition levels. Higher values represent more competitive matches.

<div align="center">

| Competition   | Competition_Level | Description | 
|-------------|-------------|--------------|
| Friendly | 1 | Least competitive (exhibition matches) |
| BMSL D3      | 2| Division 3, lowest league division  |
| BMSL Cup      | 3      | Knockout tournament with mixed opponent strength | 
| BMSL D2      | 4      | Division 2, higher level of competition |
| KSL D2      | 5      | Most competitive league (summer league with stronger teams) |

</div>

With these changes, our dataset is now organized, consistent, and ready for analysis.

## Tableau Dashboard

To complement my analysis, I created an interactive Tableau dashboard to visualize key insights from the dataset. This dashboard highlights KPIs along with detailed breakdowns regarding individual and team performance by season, competition, and weather conditions.

Click the image below to view the interactive dashboard on Tableau Public.

<p align="center"> 
  <a href="https://public.tableau.com/app/profile/kian.kaas/viz/Soccer-stats/Dashboard12" target="_blank">
    <img src="https://github.com/user-attachments/assets/f6216624-6dd1-49bc-a612-8a4e848b9d9b" alt="Tableau Dashboard" width="800">
    
    The dashboard is interactive — viewers can filter by season, competition, and weather conditions to uncover additional insights.
  </a>
</p>

## Analysis

This analysis explores the relationship between key factors — such as competition level, weather conditions, and individual contributions — to evaluate both my team’s overall performance and my individual impact as a player. To uncover meaningful insights, I utilized visualizations to identify trends, patterns, and potential influencing factors.

The analysis is divided into two main sections:

1. **Team Performance Analysis**: Examining how external factors like competition level and weather conditions influenced team outcomes.
2. **Individual Performance Analysis**: Investigating my goal contributions, my team’s performance with & without me, and consistency over time. 

## Team Performance Analysis

### 1. Win Percentage by Competition & Weather

**Win Percentage by Competition**

**Key Insights**: 

- My team's win percentage remained stable across most competitions (**64-72%**), but dropped significantly in KSL D2 (**32%**).

**Possible Explanations**:

- **Stronger Opposition**: KSL D2 features more competitive teams, making it harder to win matches.  
- **Lack of Weekly Practices**: Unlike the Fall season, which includes weekly practices to maintain fitness and tactics, the Summer season has no scheduled training. This lack of preparation may have impacted our performance, especially against stronger opponents.
- **Impact of Player Absences**: The Summer season frequently overlaps with vacation periods, resulting in frequent absences of key players. This disrupts team chemistry and often forces lineup changes.
- **Frequent Roster Changes**: The KSL allows new players to register throughout the season, which results in frequent adjustments to our lineup. As a result, our team frequently brings in new players for tryouts, making it difficult to build chemistry with teammates.

<p align="center">
  <img src="https://github.com/user-attachments/assets/93b68f8c-587c-4083-b0c9-6128d36586ab" alt="win%-comp" width="500"> 
</p>

**Win Percentage by Weather**

**Key Insights**: 

- My team’s win percentage was highest in cooler conditions, performing best in both Brisk (**68.8%**) and Rain (**68.2%**) matches.
- My team’s win percentage was lowest in Sunny conditions (**37.5%**).

**Possible Explanations**:

- **Opponent Playstyle Disruption**: Poor weather conditions may impact opponent playstyles more than ours, leading to a higher success rate for my team.
- **Competition Overlaps with Weather**: KSL D2 matches often occurred in Sunny conditions, aligning with my team’s lowest win rate. This overlap makes it difficult to isolate whether competition strength or weather had a greater impact.

<p align="center">
  <img src="https://github.com/user-attachments/assets/dded4263-f369-4ce8-bfee-610118c83f78" alt="win%-weather" width="500">  <img src="https://github.com/user-attachments/assets/ba3cfafb-393b-4f2d-8fb2-8ebb74bc6bef" alt="KSL-win%weather" width="500">
</p>

### 2. Offensive & Defensive Performance by Competition & Weather Condition

**Goals Forward & Goals Against by Competition**

**Key Insight**: My team's attacking output (1.64 goals forward per game) and defensive stability (2.91 goals against per game) are at their worst in KSL D2. 

**Possible Explanation**:

- **More Defensive Opponents**: Stronger defenses in KSL D2 limit my team's ability to create scoring chances. 
- **Tougher Opposition in Attack**: Higher-ranked teams create more scoring chances, leading to the highest goals-against rate.
- **Overall Competitive Challenge**: The combined effects of stronger defenses and offenses make KSL D2 the most difficult league to win in.

<p align="center">
  <img src="https://github.com/user-attachments/assets/cee5f7c0-1b29-4243-9894-1e57a9a19a1b" alt="goals-against-comp" width="500">   <img src="https://github.com/user-attachments/assets/d5e2dad5-a982-4f94-9a2f-b701bfdb5bf9" alt="goals-forward-comp" width="500"> 
</p>

**Goals Forward & Goals Against by Weather Condition**

**Key Insight**: My team conceded the most goals in sunny conditions (3.00 per game), while scoring output remained stable across all weather conditions. 

**Possible Explanations**: 

- **Defensive Instability in Sunny Conditions**: The increase in Goals Against in sunny conditions suggests that defensive struggles, rather than offensive inefficiencies, are the primary reason for lower win rates.  
- **Consistent Attacking Performance**: The minor variations in Goals Forward across all weather conditions suggest that offensive output is not significantly impacted by weather conditions.
- **Weather vs. Competition Effects**: The high Goals Against rate in sunny conditions may be due to many KSL D2 matches being played in sunny weather, making it difficult to isolate the impact of weather from the competition level.
- **Higher Goals Against in KSL D2**: Even in non-sunny conditions, KSL D2 consistently records some of the highest goals-against rates, accounting for three of the four highest goals conceded per game across and competition and weather combinations.

<p align="center">
  <img src="https://github.com/user-attachments/assets/a5157b3b-2f32-4d71-b970-a265cbfae102" alt="goals-forward-weather" width="500">  <img src="https://github.com/user-attachments/assets/013fcb5e-9141-44e1-907c-17e028771c4d" alt="goals-against-weather" width="500">  
  <img src="https://github.com/user-attachments/assets/308d86c3-4916-44fe-a8f6-80606b3f250f" alt="win%-comp" width="750"> 
</p>

## Individual Performance Analysis

### 1. Share of Total Team Goals

**Key Insights**:

- I have been directly involved in 35.4% of my team's total goals.
     - I account for over one-quarter of my team's goals.
     - I contribute to roughly 1 in every 3 goals that my team scores. 

**Possible Explanations**:

- **Position & Role**: As the team's first-choice striker, my role is to play in the most advanced position on the field, closest to the opponent's goal. Strikers are often the primary goal-scoring threat, positioned to finish attacking plays. My goal tally reflects this role, as I'm frequently in position to convert scoring chances. 
- **Well-Distributed Team Scoring**: With nearly two-thirds of the team’s goals scored without my involvement, it is evident that my team has a well-distributed attacking system.

<p align="center">
  <img src="https://github.com/user-attachments/assets/8d4c1f1b-1b7c-49db-9b50-00eca9c0631a" alt="Share-of-team-goals" width="500">  
</p>

### 2. Goal Contributions by Competition & Weather

**Goal Contributions by Competition**

**Key Insights**: 

- My average Goal Contributions per game decline as competition level increases, dropping from 1.22 in Friendlies to 0.50 in KSL D2.
- The sharpest drop is from BMSL D2 (1.07) to KSL D2 (0.50), showing how moving up divisions affects individual output.

**Possible Explanations**:

- **Stronger Defenses in KSL D2**: Higher-level teams allow fewer scoring opportunities.
- **Fewer Scoring Chances Overall**: Team performance also declined in KSL D2, reducing my goal-scoring involvement.
- **Competitive Matches**: The BMSL Cup also had fewer Goal Contributions per game (0.71), which makes sense as it includes knockout matches. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/2f3b0edc-02ae-4cff-a228-6c94bc8ee571" alt="goal-cont-comp" width="500"> 
</p>

**Goal Contributions by Weather Condition**

**Key Insights**: 

- My goal contributions remained fairly consistent across weather conditions, except for a significant drop in Cloudy conditions. 

**Possible Explanation**:

- **Competition Level**: Interestingly, the average competition level was very similar across weather conditions, ranging from 3.39 to 3.72. This suggests that competition was not the primary reason for lower goal contributions in Cloudy conditions.
- **Untracked Variables & Playstyle Factors**: The dataset does not include advanced statistics, such as possession or pass accuracy, which could have impacted game flow.

<p align="center">
  <img src="https://github.com/user-attachments/assets/c4ea86ea-0ca4-49bb-8ea2-e0f7704a8271" alt="goal-cont-weather" width="500"> 
</p>

**Further Analysis on Cloudy Weather Performance**

- Out of **28 games played in Cloudy conditions**:
     - 17 games (**61%**) resulted in **0** Goal Contributions.
     - 5 games (**18%**) resulted in **1** Goal Contribution. 
     - 6 games (**21%**) resulted in **2+** Goal Contributions.
- **Cloudy weather led to the most extreme fluctuations in performance**. While a small number of games (21%) resulted in high contributions (2+ G/A), the overwhelming majority (61%) ended with no goal contributions at all. This pattern suggests that Cloudy conditions were the most inconsistent and difficult to perform in.
- **Drought**: During my first year at the club, I recorded a 9-game stretch without a goal contribution in Cloudy conditions.
- **Team impact**: Throughout this 9-game stretch, my team averaged 2.0 Goals Forward per game, which is slightly below the overall 2.5 Goals Foward per game in Cloudy conditions.
     - While this may have played a role, it doesn't fully explain my lack of goal contributions in cloudy conditions.
 
**Conclusion**: 
While my performances in Cloudy conditions show significant fluctuations, the underlying cause remains unclear based on the available data. Factors such as team performance, game flow, or untracked variables may have contributed to this inconsistency. Without additional data, it is difficult to pinpoint a definitive explanation for this trend.

### 3. Individual Impact on Match Outcomes

**Key Insights**: 

- **Direct Goal Impact**: The team's win percentage significantly increases in matches where I score at least one goal (71.1%), compared to matches where I don't score (45.5%).
- **Overall Contributions Impact**: Similarly, the team has a noticeably higher win percentage in matches where I contribute (score or assist) to at least one goal, (68.9%) compared to games where I don't contribute to any goals (43.2%).

**Possible Explanations**:

- **Direct Offensive Impact**: Matches where I directly contribute to scoring (through goals or assists) significantly increase our chances of winning, underscoring my importance to the team's offensive performance. 
- **Contributions in Close Matches**: My goal contributions may frequently occur in close matches, where even a single goal or assist can decisively shift the result in our favor.

<p align="center">
  <img src="https://github.com/user-attachments/assets/6d2f518d-0b10-450c-85ac-ecbdd63c3314" alt="win%with-goal" width="500">  <img src="https://github.com/user-attachments/assets/43b875a2-1422-4c26-9f22-911bbc9540b2" alt="win%-with-goal-cont" width="500"> 
</p>

### 4. Team Performance in Games I Played vs. Did Not Play 

**Key Insights**: 

- My team's win percentage was notably higher in games I played (57.3%) compared to games I missed (30.4%).
- The team scored significantly more goals per game when I played (2.52 goals) versus when I was absent (1.57 goals).

**Possible Explanations**:

- **Offensive Contribution**: My on-field presence directly boosts team offensive output, evident from the higher average Goals Forward per game.
- **Team Confidence & Chemistry**: As the team's first-choice striker and leading scorer since joining, my presence likely boosts team confidence, motivation, and overall effectiveness, leading to improved outcomes when I participate..
- **Competition Level**: It's important to note that the average competition level for games I missed (4.39) was significantly higher than for games I played (3.51). This may have contributed to the lower win percentage and scoring output when I was absent.

<p align="center">
  <img src="https://github.com/user-attachments/assets/92975a10-e118-4131-a9d0-a2e51d6b4656" alt="win%-played-DNP" width="500">  <img src="https://github.com/user-attachments/assets/f8023b82-2507-43db-aae0-3cf354efc920" alt="goals-forward-played-DNP" width="500"> 
</p>

**Further Analysis on Competition Level**:

- **Persistent Win Percentage Gap**: Win percentages in the two highest level competitions, BMSL D2 and KSL D2, remained greater in games I played compared to games I did not play.

<p align="center">
 <img src="https://github.com/user-attachments/assets/4b6bec32-49f1-4939-b7c0-59a7544eae52" alt="win%-KSLD2-BMSLD2" width="500">  
</p>

### 5. Goal Contributions by Margin of Victory/Defeat 

**Key Insights:**

- My average goal contributions per game increase significantly as the margin of victory or defeat increases.
- My contributions notably decrease in tightly contested matches (draws or 1-goal games). 

**Possible Explanations**:

- **Increased defensive vulernability**: When teams fall behind by multiple goals, they must take greater attacking risks to recover. This inevitably leads to defensive vulnerability, exposing gaps that attacking players can exploit, particularly through counter-attacks.
- **Variation in Defensive Intensity**: Teams significantly ahead or behind often experience reduced defensive discipline—whether due to complacency (winning side) or frustration and fatigue (losing side)—further increasing attacking opportunities.  
- **Team Tactical Approach**: In tight matches, our team may adopt a more cautious strategy, affecting offensive output and limiting goal-scoring chances.
 
<p align="center">
  <img src="https://github.com/user-attachments/assets/9ddce449-e260-4342-8dde-41838ae386b3" alt="Goal-cont-margin" width="500">  
</p>

### 6. Goal Contribution Streaks and Droughts 

**Key Insights**:

- I have experienced multiple streaks of consecutive games with a goal contribution, with most streaks lasting 2-3 games and some extending to 4-5 games.
- When I snap a goal contribution drought, I am highly likely to continue contributing in the following game(s).
- While I once went 8 consecutive games without a goal contribution, this appears to be an outlier, as most of my droughts are limited to 1-2 games, highlighting my consistency across seasons.

**Possible Explanations**:

- **Momentum and Confidence**: Players often perform best when they are "in form." My tendency to extend streaks after ending a drought suggests that confidence and momentum may drive my performance.
- **Recovery**: The fact that most droughts are brief (1-2 games) suggests that even when I fail to register a goal contribution, I remain actively involved in attacking and putting myself in scoring positions.
- **Longer Droughts**: My 8-game drought may have been influenced by various factors such as stronger opposition or fitness struggles — standing out as a rare anomaly in an otherwise consistent record.

<p align="center">
  <img src="https://github.com/user-attachments/assets/1238fd48-ca8b-403e-969b-b5bd258fe9ff" alt="streaks" width="500">  <img src="https://github.com/user-attachments/assets/c3040e93-44f0-4188-9542-3273c09f508b" alt="droughts" width="500">  
</p>

**Further Analysis on the 8-game Drought**: 

- **Challenging Competition**: The average competition score during this stretch was 4.25 (1 game in BMSL Cup, 1 Friendly game, and 6 games in KSL D2). 
- **Disrupted Fitness and Form**: During this period, I took two separate trips that disrupted my playing rhythm and fitness:
     - A 10-day trip to Mexico where I missed 2 games.
     - A 1-week trip to Montreal where I missed 1 game.
- **Reduced Playing Time**: After returning from these trips, I likely played reduced minutes in the following matches due to a combination of fitness concerns and rust, further limiting my impact on the field.

**Conclusion**: 
The combination of tougher competition, interrupted fitness, and reduced playing time created challenging conditions that contributed to this extended drought. Given these circumstances, this drought appears to be an outlier rather than a reflection of my typical performance.



## Summary of Key Findings

This project revealed several meaningful insights about both my individual and my team's performance over the past three years. By combining key performance metrics with contextual factors such as competition level and weather conditions, I was able to identify notable trends and patterns. The following insights summarize the most impactful findings:

### **1. Team Performance Declined Against Stronger Competition**

**Key Finding**: My team's win percentage dropped by over **30%** in KSL D2 when compared to other competitions. 

- This decline aligned with my team’s lowest average goals forward per game (**1.64**), highlighting offensive struggles against tougher opponents.
- Additionally, my team’s goals against per game was highest in KSL D2 (**2.91**), indicating defensive challenges as well.

**Next Steps**: To improve performance during the Summer season, my team should focus on maintaining fitness and organizing weekly practices, while also improving roster stability heading into the season.

### **2. My Presence Positively Influenced Team Performance**

**Key Finding**: My presence on the field significantly improved team performance. 

- Win percentage is **27%** higher in games I played compared to games I missed.
- My team scored **0.95** more goals per game on average in games I played compared to games I missed. 
- In games I played, I was directly involved in **35.4%** of my team's total goals, contributing to just over **1 in every 3 goals** my team scores. 

**Next Steps**: To sustain this positive impact, my team should prioritize lineup stability in important matches and focus on tactics that maximize offensive consistency. 

























## Limitations


