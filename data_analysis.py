# IMPORTING
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import date, datetime

# process start time
start = time.time()

# printing out status of data
print(f"\nstatus of data: {datetime(2024, 4, 2).date()}")
print(f"today's date: {date.today()}")
print(f"difference in days: {date.today()-datetime(2024, 4, 2).date()}")

# define data
data = {
    "Name": np.array(['Ruud van Nistelrooy', 'Gerd Müller', 'Sir Bobby Charlton', 'Miroslav Klose', 'Robert Lewandowski', 'Lionel Messi', 'Cristiano Ronaldo', 'Pele', 'Harry Kane', 'Diego Maradona', 'Sergio Aguero']),
    "Nationality": np.array(['Netherlands', 'Germany', 'England', 'Germany', 'Poland', 'Argentina', 'Portugal', 'Brazil', 'England', 'Argentina', 'Argentina']),
    "Born": np.array(['07/01/1976', '11/03/1945', '10/11/1937', '06/09/1978', '08/21/1988', '06/24/1987', '02/05/1985', '10/23/1940', '07/28/1993', '10/30/1960', '06/02/1988']),
    "Career_Goals": np.array([331, 568, 233, 256, 401, 506, 538, 1279, 269, 160, 385]),
    "Career_Games": np.array([523, 611, 690, 666, 536, 609, 690, 1363, 416, 344, 685]),
    "Active": np.array(['No', 'No', 'No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'No'])
}
'''
The table contains data about soccer players, where they're from, when they're born, how many goals they scored throughout their career and how many games they played.
Since some of the players are still actice, I printed the date of when I researched the data (04/02/2024).
'''

# creating pandas DataFrame
df = pd.DataFrame(data)

# saving the DataFrame to a CSV file
df.to_csv("dataset.csv", index=False)

# printing out info about given data frame
print("\n")
df.info()
'''
data frame has 5 columns and 11 entries
2 columns consist of integers and 3 of objects
all of the given entries are non-nulls
'''

# printing out data frame
print('\n')
print(df)

# printing mean, median, mode, and standard deviation for Career_Goals
print(f"\nStatistical Analysis for Career_Goals:")
print(f"Mean: {df['Career_Goals'].mean()}")
print(f"Median: {df['Career_Goals'].median()}")
print(f"Mode: {df['Career_Goals'].mode()[0]}")
print(f"Standard Deviation: {df['Career_Goals'].std()}")
print(f"Minimum: {df['Career_Goals'].min()}")
print(f"Maximum: {df['Career_Goals'].max()}")
'''
On Average, the players scored 447.82 goals in their careers. After sorting the values ascending, the middle value is 385 goals. There you can see
that the average of goals was pulled up by the amount of Pele's goals. The mode is shown as 160. But since there is no number that appears more than
once (also not 160), the mode is considered as 0. One indicator that obviously shows, that there might be something wrong with the given mode is, that 
the mode equals the minimum of data series of Career_Goals. The standard deviation shows how much the values in the series deviate from the mean. In
this case the deviation is about 305.67, which is pretty high considering the values are between 160 and 1,279. The reason for that might again be the
high amount of goals scored by Pele.
'''

# printing mean, median, mode, and standard deviation for Career_Games
print(f"\nStatistical Analysis for Career_Games:")
print(f"Mean: {df['Career_Games'].mean()}")
print(f"Median: {df['Career_Games'].median()}")
print(f"Mode: {df['Career_Games'].mode()[0]}")
print(f"Standard Deviation: {df['Career_Games'].std()}")
print(f"Minimum: {df['Career_Games'].min()}")
print(f"Maximum: {df['Career_Games'].max()}")
'''
On Average, the players played 648.45 games in their careers. After sorting the values ascending, the middle value is 611 games. In this case, mean
and median are pretty close to each other. The mode is 690. In this series there are actually two values that equal 690, which is also the most for
same values. The standard deviation shows how much the values in the series deviate from the mean. In this case the deviation is about 263.40, which 
is still pretty high considering the values are between 344 and 1,363. The reason for that might be the high amount of games played by Pele.
'''

# histogram of Career_Goals column
bins = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300])
plt.hist(df['Career_Goals'], bins, color='r')
plt.title("Number of Players scoring certain amount of Career Goals", fontweight='bold')
plt.xlabel("Amount of Goals")
plt.ylabel("Amount of Players")
plt.show()
'''
In the plotted histogram you can see the distribution of how many players have scored goals in a certain range, divided by steps of 100. You can
see that almost all of the players are in the range of 100-600 goals, whereas there's one outlier with Pele. This indicates an exceptional performance
throughout the whole career, scoring so many more goals than other greats of soccer. 
'''

# printing process time
print(f"\nProcess finished -- {time.time()-start} seconds --")