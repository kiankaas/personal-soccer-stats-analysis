# My Soccer Stats: A Breakdown

## Introduction
Hello World! I've loved the game of soccer for as long as I can remember. I joined my first team 5 years old, playing competitively until I was 18. After a 3-year break, I returned to the pitch in 2021 where I have since played as a striker for Fraser Mills FC United, a Burnaby-based team, who now go by the name Big Fish Juve FC. 
I never used to track my stats, but as my interest in data grew, I became fascinated with advanced statistics and the insights they can provide. I began paying close attention to tracking statistics, match scores, and trends from professional teams and players, which motivated me to start manually tracking my own performance. 
This repository serves as a mini project where I will dive into some analysis on my personal soccer stats. While it’s not meant to be a large-scale project, as my dataset only contains 3 years of game data, I’m excited to uncover trends and patterns through the analysis of basic stats such as goals, assists, and match scores. 

## Background
My team competes in two leagues each year: the Burnaby Mens Soccer League (BMSL) during the Fall, and the Knight Soccer League (KSL) during the Summer. The Fall season runs from September-March, and the Summer season runs from April-August. Both leagues are divided into skill-based divisions, with Division 1 (D1) being the highest level of competition, followed by Division 2 (D2) and Division 3 (D3) respectively. In addition to the regular league matches, friendly games are also arranged throughout the year, typically between seasons. The BMSL also hosts a tournament-style cup every season, adding an extra competitive edge to the year. Although I only track basic stats, as I don't have access to my own advanced data/statistics, this project allows me to apply data analysis techniques to explore my performance across different seasons and leagues, even with a smaller dataset.

## The Data
I manually tracked my soccer stats in a Google Sheets file, which I later exported as a CSV file titled [link]raw_soccer_stats.csv. The dataset contains a comprehensive record of every game my team has played, spanning 105 records across 9 columns. Each record represents a game, capturing key statistics like goals, assists, and match outcomes, among other details as shown below.

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

This dataset provides a solid foundation for analyzing my performance throughout the seasons, uncovering patterns, and identifying key metrics that directly influenced game outcomes. While it primarily includes basic statistics, I will aim to apply various data analysis techniques to gain insights into trends and my performance over the last 3 years.

### Data Exploration, Cleaning, and Transformation
Before diving into the analysis, it is essential to prepare the dataset by exploring its structure, identifying any inconsistencies, and transforming the data as needed for a better analysis. This process includes checking for missing values, ensuring the consistency of data formats, and converting categorical variables into usable formats.

After running some queries and exploring the data, here are what I discovered:

1. There are **5** possible outcomes for **Match_Result**: D (draw), L (loss), W (win), PKL (loss via penalty shoot-out), and PKW (win via penalty shoot-out).
2. I've played in **3 Fall seasons** and **3 Summer seasons**: Fall 21/22, 22/23, 23/24 and Sum 22, 23, 24.
3. I've participated in **5 competitions**: BMSL D3, BMSL D2, BMSL Cup, KSL D2, and Friendlies.
4. The **Min** and **Max** values for **Goals_Forward** are 0 and 9 respectively. The **Min** and **Max** values for **Goals_Against** are 0 and 7 respectively. No errors here.
5. The goal and assists columns are of string data types as I games I didnt play in are marked DNP. Null values represent 0.
6. 
7. 



















