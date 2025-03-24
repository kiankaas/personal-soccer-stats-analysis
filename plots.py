import pandas as pd
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
import math
import numpy as np


# Load the cleaned dataset
df = pd.read_csv("clean_stats.csv")
df_played = df[df['Played'] == 'Yes']
df_not_played = df[df['Played'] == 'No']


# Plot: Win Percentage in Games I Played vs. Did Not Play
# Individual stats
games_played_total = len(df_played)
games_played_wins = df_played[df_played['Match_Result'].isin(['W', 'PKW'])].shape[0]
win_percentage_played = (games_played_wins / games_played_total) * 100

# Games NOT played are marked with 'DNP' in raw dataset
games_not_played_total = len(df_not_played)
games_not_played_wins = df_not_played[df_not_played['Match_Result'].isin(['W', 'PKW'])].shape[0]
win_percentage_not_played = (games_not_played_wins / games_not_played_total) * 100

# Data for plotting
categories = ['Played', 'Did Not Play']
win_percentages = [win_percentage_played, win_percentage_not_played]
games_played = [games_played_total, games_not_played_total]

# Plotting
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(categories, win_percentages, color=['green', 'red'])

# Adding data labels
for bar, percentage, games in zip(bars, win_percentages, games_played):
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{percentage:.1f}% ({games} games)", ha='center', fontsize=12, fontweight='bold')

# Formatting the plot
ax.set_ylim(0, 100)
ax.set_ylabel('Win Percentage', fontsize=12)
ax.set_title('Win Percentage in Games I Played vs. Did Not Play', fontsize=14, fontweight='bold')

plt.show()
# --- Done ---


# Plot: Win Percentage in KSL D2 & BMSL D2 for Games I Played vs. Did Not Play
# Filter for BMSL D2 and KSL D2
filtered_df = df[df['Competition'].isin(['BMSL D2', 'KSL D2'])]

# Identify wins (W or PKW)
filtered_df['Win'] = filtered_df['Match_Result'].isin(['W', 'PKW'])

# Group by competition and match participation
win_data = filtered_df.groupby(['Competition', 'Played']).agg(
    win_percentage=('Win', 'mean'),
    game_count=('Win', 'count')
).reset_index()

# Create the plot
plt.figure(figsize=(8, 5))

# Plotting
colors = ['green', 'red']  # Green for played, Red for didn't play
for i, comp in enumerate(['BMSL D2', 'KSL D2']):
    played = win_data[(win_data['Competition'] == comp) & (win_data['Played'] == 'Yes')]
    not_played = win_data[(win_data['Competition'] == comp) & (win_data['Played'] == 'No')]

    plt.bar(i - 0.15, played['win_percentage'].values[0] * 100, width=0.3, color=colors[0], label='Played' if i == 0 else "")
    plt.bar(i + 0.15, not_played['win_percentage'].values[0] * 100, width=0.3, color=colors[1], label='Did Not Play' if i == 0 else "")

    # Annotate the win percentages
    plt.text(i - 0.15, played['win_percentage'].values[0] * 100 + 1, 
             f"{played['win_percentage'].values[0]*100:.1f}%\n({played['game_count'].values[0]} games)", 
             ha='center', fontsize=12, fontweight='bold')
    plt.text(i + 0.15, not_played['win_percentage'].values[0] * 100 + 1, 
             f"{not_played['win_percentage'].values[0]*100:.1f}%\n({not_played['game_count'].values[0]} games)", 
             ha='center', fontsize=12, fontweight='bold')

# Format the plot
plt.title('Win Percentage in KSL D2 & BMSL D2 for Games I Played vs. Did Not Play', fontsize=14, fontweight='bold')
plt.xticks([0, 1], ['BMSL D2', 'KSL D2'])
plt.ylabel('Win Percentage')
plt.xlabel('Competition')
plt.ylim(0, 100)
plt.legend()

plt.show()
# --- Done ---


# Plot: Average Goals Forward in Games I Played vs. Did Not Play
# Games Played
avg_goals_forward_played = df_played['Goals_Forward'].mean()
games_played = len(df_played)

# Games Not Played
avg_goals_forward_not_played = df_not_played['Goals_Forward'].mean()

# Plotting
fig, ax = plt.subplots(figsize=(8, 6))

categories = ['Played', 'Did Not Play']
avg_goals_forward = [avg_goals_forward_played, avg_goals_forward_not_played]
bars = ax.bar(categories, avg_goals_forward, color=['green', 'red'])

# Adding data labels (average goals forward per game & number of games)
for bar, goals, games in zip(bars, avg_goals_forward, [games_played, games_not_played_total]):
    ax.text(bar.get_x() + bar.get_width()/2, goals + 0.05, f"{goals:.2f} ({games} games)", 
            ha='center', fontsize=12, fontweight='bold')

ax.set_ylabel('Goals Forward', fontsize=12)
ax.set_title('Average Goals Forward in Games I Played vs. Did Not Play', fontsize=14, fontweight='bold')
ax.set_ylim(0, max(avg_goals_forward) + 1)
plt.show()
# --- Done ---


# Plot: Average Goal Contributions by Margin of Victory/Defeat
# Calculate goal margin
df_played["Goal_Margin"] = (df_played["Goals_Forward"] - df_played["Goals_Against"]).abs()

# Categorize games based on goal margin
def categorize_margin(row):
    if row["Goal_Margin"] == 0:
        return "0 goals (Draw)"
    elif row["Goal_Margin"] == 1:
        return "1 goal"
    elif row["Goal_Margin"] == 2:
        return "2 goals"
    else:
        return "3+ goals"

df_played["Margin_Category"] = df_played.apply(categorize_margin, axis=1)
# Calculate average goal contributions by margin category
goal_contrib_avg = df_played.groupby("Margin_Category")["Goal_Contributions"].mean()

# Total games played per category
games_played = df_played["Margin_Category"].value_counts()

# Categories ordered logically
categories_order = ["0 goals (Draw)", "1 goal", "2 goals", "3+ goals"]
goal_contrib_avg = goal_contrib_avg.reindex(categories_order)
games_played = games_played.reindex(categories_order)

# Plotting
plt.figure(figsize=(8, 6))
bars = plt.bar(goal_contrib_avg.index, goal_contrib_avg.values, color='green')

# Annotate bar values
for bar, games_played in zip(bars, games_played):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
             f"{bar.get_height():.2f} ({games_played} games)", ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title("Average Goal Contributions per Game by Margin of Victory/Defeat", fontsize=14, fontweight='bold')
plt.xlabel("Margin of Victory/Defeat", fontsize=14)
plt.ylabel("Goal Contributions", fontsize=14)
plt.ylim(0, goal_contrib_avg.max() + 0.5)

plt.show()
# --- Done ---


# Pie chart: My Share of Total Team Goals 
# Calculate values
my_goals = df_played["Goals"].sum()
my_assists = df_played["Assists"].sum()
total_team_goals = df_played["Goals_Forward"].sum()
uninvolved_goals = total_team_goals - my_goals - my_assists

# Data for Pie Chart (updated labels with counts)
labels = [
    f"My Goals ({my_goals})", 
    f"My Assists ({my_assists})", 
    f"Goals Without My\nInvolvement ({uninvolved_goals})"
]
sizes = [my_goals, my_assists, uninvolved_goals]
colors = ["tab:green", "lightgreen", "#90A4AE"]
explode = (0.07, 0.07, 0)

# Create pie chart
plt.figure(figsize=(6, 6))
wedges, texts, autotexts = plt.pie(
    sizes, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%',
    shadow=True, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'}
)

plt.title("My Share of Total Team Goals", fontsize=16, fontweight='bold')
plt.axis('equal')
plt.show()
# --- Done ---


# Plot: Streaks: Consecutive Games with a Goal Contribution by Length
streaks = []
current_streak = 0

for value in df_played['Goal_Contributions']:
    if value:  # If a goal contribution happened
        current_streak += 1
    else:  # End of a streak
        if current_streak > 0:
            streaks.append(current_streak)
        current_streak = 0

# If the final entries are part of a streak, capture the last streak
if current_streak > 0:
    streaks.append(current_streak)

# Create a frequency count of streak lengths
streak_counts = pd.Series(streaks).value_counts().sort_index()

# Plotting
plt.figure(figsize=(8, 6))
bars = plt.bar(streak_counts.index, streak_counts.values, color='tab:green')

# Annotate bar values
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, int(yval),
             ha='center', va='bottom', fontsize=12, fontweight='bold')

# Chart details
plt.title("Streaks: Consecutive Games with a Goal Contribution", fontsize=14, fontweight='bold')
plt.xlabel("Streak Length (Games)", fontsize=12)
plt.ylabel("Number of Streaks", fontsize=12)
plt.ylim(0, streak_counts.max() + 0.5)

plt.show()
# --- Done ---

# Plot: Droughts: Consecutive Games without a Goal Contribution
# Identify drought streaks
drought_lengths = []
current_drought = 0

for contributed in df_played['Goal_Contributions']:
    if not contributed:  # If no goal contribution
        current_drought += 1
    else:
        if current_drought > 0:
            drought_lengths.append(current_drought)
        current_drought = 0  # Reset if contribution found

# Capture any drought that ends at the final game
if current_drought > 0:
    drought_lengths.append(current_drought)

# Count occurrences of each drought length
drought_counts = pd.Series(drought_lengths).value_counts().sort_index()

# Plotting
plt.figure(figsize=(8, 6))
bars = plt.bar(drought_counts.index, drought_counts.values, color='red')

# Annotate bar values
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), 
             ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title("Droughts: Consecutive Games without a Goal Contribution", fontsize=14, fontweight='bold')
plt.xlabel("Drought Length (Games)", fontsize=12)
plt.ylabel("Number of Droughts", fontsize=12)
plt.ylim(0, drought_counts.max() + 0.5)

plt.show()
# --- Done ---


# Plot: Win Percentage by Weather Condition
# Calculate win percentage by weather condition
weather_performance = df.groupby("Weather").agg(
    Win_Percentage=("Match_Result", lambda x: ((x == "W").sum() + (x == "PKW").sum()) / len(x) * 100)
)

# Sort weather categories for clarity
weather_order = ["Rain", "Brisk", "Cloudy", "Sunny"]
weather_performance = weather_performance.reindex(weather_order)

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(weather_performance.index, weather_performance["Win_Percentage"], color="green")

# Add win % labels above bars
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f"{bar.get_height():.1f}%", ha="center", fontsize=12, fontweight="bold")

# Labels and title
plt.xlabel("Weather Condition", fontsize=12)
plt.ylabel("Win Percentage", fontsize=12)
plt.title("Win Percentage by Weather Condition", fontsize=14, fontweight="bold")
plt.ylim(0, 100)
plt.xticks(rotation=45, fontsize=11)
plt.yticks(fontsize=11)

# Show graph
plt.show()
# --- Done ---


# Plot: Win Percentage in KSL D2 by Weather Condition
# Filter dataset for only KSL D2 games
ksl_d2_df = df[df["Competition"] == "KSL D2"]

# Calculate win percentage and number of games played by weather condition
ksl_d2_weather_performance = ksl_d2_df.groupby("Weather").agg(
    Win_Percentage=("Match_Result", lambda x: ((x == "W").sum() + (x == "PKW").sum()) / len(x) * 100),
    Games_Played=("Match_Result", "count")  # Count number of games per weather condition
)

# Ensure all weather categories are included, filling missing values with 0
ksl_d2_weather_performance = ksl_d2_weather_performance.reindex(weather_order).fillna(0)

# Convert games played to integers
ksl_d2_weather_performance["Games_Played"] = ksl_d2_weather_performance["Games_Played"].astype(int)

# Store a copy for labeling purposes (so we can display "N/A" when no games were played)
ksl_d2_weather_performance["Win_Label"] = ksl_d2_weather_performance.apply(
    lambda row: "N/A" if row["Games_Played"] == 0 else f"{row['Win_Percentage']:.1f}%",
    axis=1
)

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(ksl_d2_weather_performance.index, ksl_d2_weather_performance["Win_Percentage"], color="green")

# Add labels above bars (Win % and Games Played)
for bar, (win_label, games) in zip(bars, ksl_d2_weather_performance[["Win_Label", "Games_Played"]].itertuples(index=False)):
    # Adjust text to show 'game' instead of 'games' when only 1 game is played
    game_text = "game" if games == 1 else "games"
    
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, 
             f"{win_label} ({games} {game_text})", 
             ha="center", fontsize=12, fontweight="bold")


# Labels and title
plt.xlabel("Weather Condition", fontsize=12)
plt.ylabel("Win Percentage", fontsize=12)
plt.title("Win Percentage in KSL D2 by Weather Condition", fontsize=14, fontweight="bold")
plt.ylim(0, 100)
plt.xticks(rotation=45, fontsize=11)
plt.yticks(fontsize=11)

# Show graph
plt.show()
# --- Done ---


# Plot: Win Percentage in Matches With vs. Without Goal Contributions
# Identify matches with and without goal contributions
df_played['With_GC'] = df_played['Goal_Contributions'] > 0

# Calculate win percentage
win_data = df_played.groupby('With_GC').agg(
    win_percentage=('Match_Result', lambda x: (x.isin(['W', 'PKW']).mean()) * 100),
    game_count=('Match_Result', 'count')
).reset_index()

# Map values for clarity and reorder the DataFrame
win_data['Label'] = win_data['With_GC'].map({True: '1+ Goal Contributions', False: '0 Goal Contributions'})
win_data = win_data.sort_values(by='With_GC', ascending=False) 

# Create the plot
plt.figure(figsize=(6, 4))

bars = plt.bar(win_data['Label'], win_data['win_percentage'], color=['green', 'red'])

# Annotate bars
for bar, (win_label, games) in zip(bars, win_data[['win_percentage', 'game_count']].itertuples(index=False)):
    game_text = "1 game" if games == 1 else f"{games} games"
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f"{win_label:.1f}%\n({game_text})", ha='center', fontsize=12, fontweight='bold')

# Format the plot
plt.title('Win Percentage in Matches With vs. Without Goal Contributions', fontsize=14, fontweight='bold')
plt.ylabel('Win Percentage')
plt.ylim(0, 100)
plt.show()
# --- done ---

# Plot: Win Percentage in Matches Where I Scored vs. Didn't Score
# Identify matches with and without goal contributions
df_played['With_Goal'] = df_played['Goals'] > 0

# Calculate win percentage
win_data = df_played.groupby('With_Goal').agg(
    win_percentage=('Match_Result', lambda x: (x.isin(['W', 'PKW']).mean()) * 100),
    game_count=('Match_Result', 'count')
).reset_index()

# Map values for clarity and reorder the DataFrame
win_data['Label'] = win_data['With_Goal'].map({True: '1+ Goal Contributions', False: '0 Goal Contributions'})
win_data = win_data.sort_values(by='With_Goal', ascending=False) 

# Create the plot
plt.figure(figsize=(6, 4))

bars = plt.bar(win_data['Label'], win_data['win_percentage'], color=['green', 'red'])

# Annotate bars
for bar, (win_label, games) in zip(bars, win_data[['win_percentage', 'game_count']].itertuples(index=False)):
    game_text = "1 game" if games == 1 else f"{games} games"
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f"{win_label:.1f}%\n({game_text})", ha='center', fontsize=12, fontweight='bold')

# Format the plot
plt.title("Win Percentage in Matches Where I Scored vs. Didn't Score", fontsize=14, fontweight='bold')
plt.ylabel('Win Percentage')
plt.ylim(0, 100)
plt.show()
# --- done ---


# Plot: Win Percentage by Competition
# Calculate win percentage by competition level
competition_performance = df.groupby("Competition").agg(
    Win_Percentage=("Match_Result", lambda x: ((x == "W").sum() + (x == "PKW").sum()) / len(x) * 100)
)

# Sort by competition difficulty
competition_performance = competition_performance.reindex(["Friendly", "BMSL D3", "BMSL Cup", "BMSL D2", "KSL D2"])

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(competition_performance.index, competition_performance["Win_Percentage"], color="green")

# Add win % labels above bars
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f"{bar.get_height():.1f}%", ha="center", fontsize=12, fontweight="bold")

# Labels and title
plt.xlabel("Competition", fontsize=12)
plt.ylabel("Win Percentage", fontsize=12)
plt.title("Win Percentage by Competition", fontsize=14, fontweight="bold")
plt.ylim(0, 100)
plt.xticks(rotation=45, fontsize=11)
plt.yticks(fontsize=11)

# Show graph
plt.show()
# --- Done --- 


# Plot: Average Goal Contributions per Game by Competition
# Calculate Average Goal Contributions per Game by Competition
avg_goal_contributions = df_played.groupby("Competition")["Goal_Contributions"].mean()

# Sort by competition difficulty
competition_order = ["Friendly", "BMSL D3", "BMSL Cup", "BMSL D2", "KSL D2"]
avg_goal_contributions = avg_goal_contributions.reindex(competition_order)

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(avg_goal_contributions.index, avg_goal_contributions, color="tab:green")

# Add labels above bars
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
             f"{bar.get_height():.2f}", ha="center", fontsize=12, fontweight="bold")

# Labels and title
plt.xlabel("Competition", fontsize=12)
plt.ylabel("Goal Contributions", fontsize=12)
plt.title("Average Goal Contributions per Game by Competition", fontsize=14, fontweight="bold")
plt.ylim(0, max(avg_goal_contributions) + 0.5)
plt.xticks(rotation=45, fontsize=11)
plt.yticks(fontsize=11)

plt.show()
# --- Done ---


# Plot: Average Goal Contributions per Game by Weather Condition
# Calculate Average Goal Contributions per Game by Competition
avg_goal_contributions_weather = df_played.groupby("Weather")["Goal_Contributions"].mean()

# Sort by competition difficulty
avg_goal_contributions_weather = avg_goal_contributions_weather.reindex(weather_order)

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(avg_goal_contributions_weather.index, avg_goal_contributions_weather, color="tab:green")

# Add labels above bars
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
             f"{bar.get_height():.2f}", ha="center", fontsize=12, fontweight="bold")

# Labels and title
plt.xlabel("Weather Condition", fontsize=12)
plt.ylabel("Goal Contributions", fontsize=12)
plt.title("Average Goal Contributions per Game by Weather Condition", fontsize=14, fontweight="bold")
plt.ylim(0, max(avg_goal_contributions_weather) + 0.5)
plt.xticks(rotation=45, fontsize=11)
plt.yticks(fontsize=11)

plt.show()
# --- Done ---


# Plot: Games Played in Sunny Conditions by Competition
# Filter for Sunny conditions
sunny_games = df[df['Weather'] == 'Sunny']

# Create a list of all competitions to ensure BMSL D3 is included
all_competitions = ['Friendly', 'BMSL D3', 'BMSL Cup', 'BMSL D2', 'KSL D2']

# Count games played in Sunny conditions by competition
sunny_distribution = sunny_games['Competition'].value_counts().reindex(all_competitions, fill_value=0)

# Plotting
plt.figure(figsize=(8, 5))
bars = plt.bar(sunny_distribution.index, sunny_distribution.values, color='yellow', edgecolor='black')

# Add labels on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, f'{int(yval)}', ha='center', fontsize=12, fontweight='bold')

# Formatting
plt.title('Games Played in Sunny Conditions by Competition', fontsize=14, fontweight='bold')
plt.xlabel('Competition')
plt.ylabel('Games Played')
plt.ylim(0, max(sunny_distribution.values) + 2) 
plt.xticks(rotation=45, fontsize=11)
plt.yticks(fontsize=11)
plt.show()
# --- Done ---


# Plot: Average Goals Against per Game by Competition
avg_goals_against_comp = df.groupby("Competition")["Goals_Against"].mean()
avg_goals_against_comp = avg_goals_against_comp.reindex(competition_order)

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(avg_goals_against_comp.index, avg_goals_against_comp, color="red")

# Add labels above bars
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
             f"{bar.get_height():.2f}", ha="center", fontsize=12, fontweight="bold")

# Labels and title
plt.xlabel("Competition", fontsize=12)
plt.ylabel("Goals Against", fontsize=12)
plt.title("Average Goals Against per Game by Competition", fontsize=14, fontweight="bold")
plt.ylim(0, max(avg_goals_against_comp) + 0.5)
plt.xticks(rotation=45, fontsize=11)
plt.yticks(fontsize=11)

# Show graph
plt.show()
# --- Done ---


# Plot: Average Goals Forward per Game by Competition
avg_goals_forward_comp = df.groupby("Competition")["Goals_Forward"].mean()
avg_goals_forward_comp = avg_goals_forward_comp.reindex(competition_order)

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(avg_goals_forward_comp.index, avg_goals_forward_comp, color="blue")

# Add labels above bars
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
             f"{bar.get_height():.2f}", ha="center", fontsize=12, fontweight="bold")

# Labels and title
plt.xlabel("Competition", fontsize=12)
plt.ylabel("Goals Forward", fontsize=12)
plt.title("Average Goals Forward per Game by Competition", fontsize=14, fontweight="bold")
plt.ylim(0, max(avg_goals_forward_comp) + 0.5)
plt.xticks(rotation=45, fontsize=11)
plt.yticks(fontsize=11)

plt.show()
# --- Done ---


# Plot: Average Goals Against per Game by Weather Condition
avg_goals_against_weather = df.groupby("Weather")["Goals_Against"].mean()

# Sort weather categories for consistency
avg_goals_against_weather = avg_goals_against_weather.reindex(weather_order)

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(avg_goals_against_weather.index, avg_goals_against_weather, color="red")

# Add labels above bars
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
             f"{bar.get_height():.2f}", ha="center", fontsize=12, fontweight="bold")

# Labels and title
plt.xlabel("Weather Condition", fontsize=12)
plt.ylabel("Goals Against", fontsize=12)
plt.title("Average Goals Against per Game by Weather Condition", fontsize=14, fontweight="bold")
plt.ylim(0, max(avg_goals_against_weather) + 0.5)
plt.xticks(rotation=45, fontsize=11)
plt.yticks(fontsize=11)

# Show graph
plt.show()
# --- Done ---


# Plot: Average Goals Forward per Game by Weather Condition
avg_goals_forward_weather = df.groupby("Weather")["Goals_Forward"].mean()

# Sort weather categories for consistency
avg_goals_forward_weather = avg_goals_forward_weather.reindex(weather_order)

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(avg_goals_forward_weather.index, avg_goals_forward_weather, color="blue")

# Add labels above bars
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
             f"{bar.get_height():.2f}", ha="center", fontsize=12, fontweight="bold")

# Labels and title
plt.xlabel("Weather Condition", fontsize=12)
plt.ylabel("Goals Forward", fontsize=12)
plt.title("Average Goals Forward per Game by Weather Condition", fontsize=14, fontweight="bold")
plt.ylim(0, max(avg_goals_against_weather) + 0.5)
plt.xticks(rotation=45, fontsize=11)
plt.yticks(fontsize=11)

plt.show()
# --- Done ---

# Find the average competition score for games I played vs. did not play
# Also find the average competition score for each weather condition later
competition_mapping = {
    "Friendly": 1,    # Least competitive
    "BMSL D3": 2,     # Division 3 (lowest division)
    "BMSL Cup": 3,    # BMSL Cup (mixed opponents)
    "BMSL D2": 4,     # Division 2 (more competitive)
    "KSL D2": 5       # Strongest competition (summer league)
}

# Encode Competition Level for games played
df['Competition'] = df['Competition'].map(competition_mapping)
avg_competition_played = df['Competition'].mean()

# Games Not Played
df_not_played['Competition'] = df_not_played['Competition'].map(competition_mapping)
avg_competition_not_played = df_not_played['Competition'].mean()

# Output results
print(f"Average Competition Score for Games Played: {avg_competition_played:.2f}")
print(f"Average Competition Score for Games Not Played: {avg_competition_not_played:.2f}")