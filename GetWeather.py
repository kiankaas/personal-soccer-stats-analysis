import requests
import pandas as pd
import time

# Load the dataset
file_path = '/Users/kiankaas/Desktop/Soccer-stats-Analysis/raw_soccer_stats.csv'
data = pd.read_csv(file_path)

# Date column is in 'dd-mm-yyyy' format
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y', errors='coerce')

# Visual Crossing API details, my API key is blocked out for privacy
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
API_KEY = "##################"  # Replace with your Visual Crossing API key
location = "Burnaby"

# Visual Crossing API gives temperature in Fahrenheit
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * (5/9)

# Lists to store the weather and temperature data
weather_data = []
temp_celsius_data = []

# Loop through the dataset and fetch weather for 6:00 PM (18:00) for each date
for index, row in data.iterrows():
    match_date = row['Date']
    
    # Format the date as YYYY-MM-DD for the API
    formatted_date = match_date.strftime('%Y-%m-%d')
    
    # Build the API request URL
    url = f"{BASE_URL}{location}/{formatted_date}?key={API_KEY}"
    
    # Make the API request
    response = requests.get(url)
    response_json = response.json()
    #print(response_json)
    
    # Extract the weather for 6:00 PM (18:00)
    if 'days' in response_json:
        hourly_data = response_json['days'][0]['hours']
        
        # Find the 6:00 PM (18:00) data
        for hour in hourly_data:
            if hour['datetime'] == "18:00:00":  # Check for 6:00 PM
                temp_fahrenheit = hour['temp']  # Temperature in Fahrenheit
                temp_celsius = fahrenheit_to_celsius(temp_fahrenheit)  # Convert to Celsius
                weather = hour['conditions']  # Weather conditions (e.g., 'Rain', 'Clear')        
    
    # Append the extracted data to the lists
    weather_data.append(weather)
    temp_celsius_data.append(round(temp_celsius) if temp_celsius is not None else 'N/A')
    
    # Optional: Add a sleep to avoid API rate limits (1 request per second)
    time.sleep(1)

# Add the weather and temperature data as new columns in the dataset
data['Weather'] = weather_data
data['Temperature'] = temp_celsius_data

# Save the updated dataset to a new CSV file
output_file_path = '/Users/kiankaas/Desktop/Soccer-stats-Analysis/updated_raw_stats.csv'
data.to_csv(output_file_path, index=False)
