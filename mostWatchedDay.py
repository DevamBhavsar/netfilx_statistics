"""
This script analyzes the viewing activity data for a Netflix user and generates a bar chart showing the number of hours watched per weekday.

The script reads in a CSV file containing the viewing activity data, filters the data to only include the specified user, and then calculates the total hours watched per weekday. The resulting bar chart is saved to a file named 'by_day.png'.
"""
import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv("/path/to/CONTENT_INTERACTION/ViewingActivity.csv").drop(["Attributes","Supplemental Video Type","Bookmark","Latest Bookmark","Country"], axis=1)
data['Start Time'] = pd.to_datetime(data['Start Time'], utc=True)
data = data.set_index('Start Time')
data.index = data.index.tz_convert("Asia/Calcutta") 
data = data.reset_index()
data['Duration'] = pd.to_timedelta(data['Duration'])
user = data[data["Profile Name"].str.contains("user", regex=False)].copy()
user["weekday"] = user["Start Time"].dt.weekday
user["hour"] = user["Start Time"].dt.hour

print(user)     
day_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

user['weekday'] = pd.Categorical(user['weekday'].map(day_map), categories=[day_map[i] for i in range(7)], ordered=True)


by_day = user['weekday'].value_counts()
by_day = by_day.sort_index()
plt.rcParams.update({'font.size': 22})
by_day.plot(kind='bar', figsize=(20,10), title='Watched by Day')
plt.xticks(rotation=30)
plt.savefig('by_day.png')
