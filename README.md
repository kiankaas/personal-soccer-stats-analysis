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
     - **Brisk**: Used for colder, clear days, including "Clear" conditions with Temperatuer < 15°C, and "Partially cloudy" conditions with Temperatuer < 10°C. 
5. Converted the **Goals**, **Assists**, and **Goals+Assists** columns to **integer** data types.

With these changes, our dataset is now organized, consistent, and ready for analysis.

## Analysis
**SQL Query**: [link]() <br/>

To ensure meaningful analysis, categorical variables were **numerically encoded**, allowing for correlation analysis and structured comparisons across different conditions. The endcoding
choices were carefully designed to maintain logical consistency - **higher values indicate more challenging conditions** across all categories.  

### Data Encoding
**Python Script**: [link]() <br/>

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


A **weighted competition score** was calculated using the formula below for each season to reflect the combined difficulty of all competitions played during that period.

\[
\text{Season Score} = \frac{\sum (\text{Games in Competition} \times \text{Competition Score})}{\sum \text{Total Games in Season}}
\]


![Screen Shot 2025-02-22 at 5 29 57 PM](https://github.com/user-attachments/assets/eba150a1-2224-40a6-b826-99bbc6621f0d)

**Match Result** 
| Match Result   | Encoded Value | Description | 
|-------------|-------------|--------------|
| L | 0 | Loss |
| PKL      | 1 | Loss via penalty shoot-out  |
| D      | 1      | Draw | 
| PKW      | 2      | Win via penalty shoot-out |
| W      | 3      | Win |

Match results were encoded using the standard soccer point system, where teams earn 3 points for a win, 2 for a win via penalty shoot-out, 1 for a draw or loss via penalty shoot-out, and 0 for a loss.
This encoding ensures consistency with real-world soccer scoring while allowing for performance analysis.























