'''
This Python script is designed to scrape data from Worldometer's Coronavirus data page. It then saves this data both as a CSV file and into a relational 
database with two tables. Basic SQL queries are performed to among other things clean the data, ensuring that all NULL and N/A values are updated to 0. 
Subsequently, the cleaned data from the database is exported back to two CSV files. Descriptive statistical analysis, including mean, variance and standard 
deviation is conducted on the dataset. Finally, Matplotlib is utilized to visualize the data through a couple types of graphs, showcasing different columns 
of the dataset.
'''

################################# IMPORTING #################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import csv
import locale

################################# AUXILIARY FUNCTION #################################

# prints out SQL queries
def print_sql_cursor(query):
    cursor.execute(query)
    rows = cursor.fetchall() # fetch all rows from result
    for row in rows:
        print(row[0]) # access value of column in each row

################################# MAIN #################################
if __name__ == '__main__':

    # set start time
    start = time.time()

    # time after a success message
    sleep_time = 1

    # url from where data will be scratched
    url = 'https://www.worldometers.info/coronavirus/'

    # get requests to receive data from page
    html_page = requests.get(url).text

    # parse data
    soup = BeautifulSoup(html_page, 'html.parser')

    # success message
    print("\nData successfully scraped and parsed.")
    time.sleep(sleep_time)

    # extracting table data from data set
    get_table = soup.find('table', id='main_table_countries_today')

    # extracting tr tags
    get_table_data = get_table.tbody.find_all('tr')

    # creating dict that will later be transformed to dataframe
    dic = {}

    # extracting country names and all the values for each country, putting them in the created dict
    for i in range (len(get_table_data)):
        # try to find country name in a tags
        try:
            key = get_table_data[i].find_all('a', href = True)[0].string
        # try to find country name in td tags
        except:
            key = get_table_data[i].find_all('td')[0].string

        # finding values for each country
        values = [j.string for j in get_table_data[i].find_all('td')]

        # filling dict with data found
        dic[key] = values

    # Remove the first entry containing unwanted data
    dic = dict(list(dic.items())[1:])

    # Removing whitespaces from data
    for country, values in dic.items():
        cleaned_values = [value.strip() if isinstance(value, str) else value for value in values]
        dic[country] = cleaned_values

    # Removing first column and all columns coming after population column
    for country, country_values in dic.items():
        dic[country] = country_values[1:15]

    # success message
    # for key, value in dic.items():
    #   print(key, value)
    print ("\nDictionary successfully created.")
    time.sleep(sleep_time)

    # setting column names for dataframe
    column_names = ['Total Cases',	'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 'New Recovered', 'Active Cases', 'Serious, Critical',	'Tot Cases/1M pop', 'Deaths/1M pop', 'Total Tests', 'Tests/1M pop',	'Population']

    # creating dataframe, transposing data by changing rows and columns
    df = pd.DataFrame(dic).iloc[1:,:].T.iloc[:,:14]

    # sets the name of the index of dataframe to 'Country'
    df.index.name = 'Country'

    # assign column_names to dataframe columns
    df.columns = column_names

    # success message
    # print(df.head())
    print ("\nDataframe successfully created.")
    time.sleep(sleep_time)

    # save dataframe to CSV file
    df.to_csv('raw_data.csv')

    # success message
    print ("\nDataframe successfully saved to CSV file.")
    time.sleep(sleep_time)

    # create a connection to the new created SQLite database covid_data.db
    with sqlite3.connect('./covid_data.db') as conn:
        cursor = conn.cursor()

        # create CountryInfo table
        cursor.execute('''CREATE TABLE IF NOT EXISTS CountryInfo (
                            id INTEGER PRIMARY KEY,
                            country_name TEXT,
                            population INTEGER
                        )''')

        # create CovidStats table
        cursor.execute('''CREATE TABLE IF NOT EXISTS CovidStats (
                            id INTEGER PRIMARY KEY,
                            country_id INTEGER,
                            total_cases INTEGER,
                            new_cases INTEGER,
                            total_deaths INTEGER,
                            new_deaths INTEGER,
                            total_recovered INTEGER,
                            new_recovered INTEGER,
                            active_cases INTEGER,
                            serious_critical INTEGER,
                            tot_cases_1m_pop INTEGER,
                            deaths_1m_pop INTEGER,
                            total_tests INTEGER,
                            tests_1m_pop INTEGER
                        )''')

        # insert data into CountryInfo table
        country_data = [(None, country_name, None) for country_name in df.index]
        cursor.executemany('''INSERT INTO CountryInfo (id, country_name, population) VALUES (?, ?, ?)''', country_data)

        # set row factory to return rows as dictionaries
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # get the last inserted row ID for each country
        cursor.execute('''SELECT id, country_name FROM CountryInfo''')
        country_ids = {row['country_name']: row['id'] for row in cursor.fetchall()}

        # insert data into CovidStats table
        covid_data = [(country_ids[country_name], row['Total Cases'], row['New Cases'], row['Total Deaths'], row['New Deaths'], row['Total Recovered'], row['New Recovered'], row['Active Cases'], row['Serious, Critical'], row['Tot Cases/1M pop'], row['Deaths/1M pop'], row['Total Tests'], row['Tests/1M pop']) for country_name, row in df.iterrows()]
        cursor.executemany('''INSERT INTO CovidStats (country_id, total_cases, new_cases, total_deaths, new_deaths, total_recovered, new_recovered, active_cases, serious_critical, tot_cases_1m_pop, deaths_1m_pop, total_tests, tests_1m_pop) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', covid_data)

        # success message
        print("\nDatabase created and successfully filled with data.")
        time.sleep(sleep_time)

        # update null values and 'N/A' values to 0 in CountryInfo table
        cursor.execute('''UPDATE CountryInfo SET
                        population = CASE WHEN population IS NULL OR population = 'N/A' THEN 0 ELSE population END''')

        # update null values and 'N/A' values to 0 in CovidStats table
        cursor.execute('''UPDATE CovidStats SET 
                        total_cases = CASE WHEN total_cases IS NULL OR total_cases = 'N/A' THEN 0 ELSE total_cases END''')
        cursor.execute('''UPDATE CovidStats SET 
                        new_cases = CASE WHEN new_cases IS NULL OR new_cases = 'N/A' THEN 0 ELSE new_cases END''')
        cursor.execute('''UPDATE CovidStats SET 
                        total_deaths = CASE WHEN total_deaths IS NULL OR total_deaths = 'N/A' THEN 0 ELSE total_deaths END''')
        cursor.execute('''UPDATE CovidStats SET 
                        new_deaths = CASE WHEN new_deaths IS NULL OR new_deaths = 'N/A' THEN 0 ELSE new_deaths END''')
        cursor.execute('''UPDATE CovidStats SET 
                        total_recovered = CASE WHEN total_recovered IS NULL OR total_recovered = 'N/A' THEN 0 ELSE total_recovered END''')
        cursor.execute('''UPDATE CovidStats SET 
                        new_recovered = CASE WHEN new_recovered IS NULL OR new_recovered = 'N/A' THEN 0 ELSE new_recovered END''')
        cursor.execute('''UPDATE CovidStats SET 
                        active_cases = CASE WHEN active_cases IS NULL OR active_cases = 'N/A' THEN 0 ELSE active_cases END''')
        cursor.execute('''UPDATE CovidStats SET 
                        serious_critical = CASE WHEN serious_critical IS NULL OR serious_critical = 'N/A' THEN 0 ELSE serious_critical END''')
        cursor.execute('''UPDATE CovidStats SET 
                        tot_cases_1m_pop = CASE WHEN tot_cases_1m_pop IS NULL OR tot_cases_1m_pop = 'N/A' THEN 0 ELSE tot_cases_1m_pop END''')
        cursor.execute('''UPDATE CovidStats SET 
                        deaths_1m_pop = CASE WHEN deaths_1m_pop IS NULL OR deaths_1m_pop = 'N/A' THEN 0 ELSE deaths_1m_pop END''')
        cursor.execute('''UPDATE CovidStats SET 
                        total_tests = CASE WHEN total_tests IS NULL OR total_tests = 'N/A' THEN 0 ELSE total_tests END''')
        cursor.execute('''UPDATE CovidStats SET 
                        tests_1m_pop = CASE WHEN tests_1m_pop IS NULL OR tests_1m_pop = 'N/A' THEN 0 ELSE tests_1m_pop END''')
        
        # success message
        print("\nData successfully cleaned.")
        time.sleep(sleep_time)

        # announcing SQL queries
        print("\nSQL queries:")
        time.sleep(sleep_time)

        # executing some basic SQL queries
        # list containing queries
        queries = [
            '''SELECT country_name FROM CountryInfo ORDER BY country_name ASC;''', # all country_names ordered ascending
            '''SELECT total_cases FROM CovidStats LIMIT 20;''', # showing the first 20 entries of total_cases
            '''SELECT AVG(deaths_1m_pop) FROM CovidStats''', # printing mean for deaths per 1 mil population
            '''SELECT MAX(active_cases) FROM CovidStats''' # printing maximum for active_cases
        ]

        # for loop to call SQL query printing function to print out all queries
        for i in queries:
            print()
            print_sql_cursor(i)
            time.sleep(sleep_time)

        # success message
        print("\nSQL queries successfully executed.")
        time.sleep(sleep_time)

        # execute SELECT queries to fetch data from tables
        cursor.execute('''SELECT * FROM CountryInfo''')
        country_info_data = cursor.fetchall()

        cursor.execute('''SELECT * FROM CovidStats''')
        covid_stats_data = cursor.fetchall()

        # define CSV file names and paths
        country_info_csv_file = 'country_info.csv'
        covid_stats_csv_file = 'covid_stats.csv'

        # write fetched data to CSV files
        with open(country_info_csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i[0] for i in cursor.description])  # write header
            writer.writerows(country_info_data)

        with open(covid_stats_csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i[0] for i in cursor.description])  # write header
            writer.writerows(covid_stats_data)

        # success message
        print("\nDatabase tables successfully saved to CSV files.")
        time.sleep(sleep_time)

    ### Analysis and Visualization of data
    ''' values of scraped data might change over time, For this reason, I will add comments after the calculations to indicate which values I have used. 
    For the visualizations I will also submit the graphs.'''

    # reading both database tables as CSV files
    df_country_info = pd.read_csv('country_info.csv')
    df_covid_stats = pd.read_csv('covid_stats.csv')

    # success message
    print("\nCSV files successfully loaded.")
    time.sleep(sleep_time)

    # Analysis

    # columns for covid_stats in a list to iterate over them to convert them to numeric values
    covid_stats_columns = ['id', 'country_id', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered',
                            'new_recovered', 'active_cases', 'serious_critical', 'tot_cases_1m_pop', 'deaths_1m_pop',
                            'total_tests', 'tests_1m_pop']

    # set locale to US UTF-8
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')

    # convert integer values to strings, then apply locale.atof for each column, enables calculations with these values
    for col in covid_stats_columns:
        df_covid_stats[col] = df_covid_stats[col].apply(lambda x: locale.atof(str(x)))

    # printing mean, median, mode, standard deviation, variance, min and max for total_cases
    print(f"\nStatistical Analysis for total_cases:")
    print(f"Mean: {df_covid_stats['total_cases'].mean()}") # = 3050828.329004329
    print(f"Median: {df_covid_stats['total_cases'].median()}") # = 206897.0
    print(f"Mode: {df_covid_stats['total_cases'].mode()[0]}") # = 9.0
    print(f"Standard Deviation: {df_covid_stats['total_cases'].std()}") # = 10020788.9925313
    print(f"Variance: {df_covid_stats['total_cases'].var()}") # = 100416212032836.47
    print(f"Minimum: {df_covid_stats['total_cases'].min()}") # = 9.0
    print(f"Maximum: {df_covid_stats['total_cases'].max()}") # = 111810548.0
    '''
    The analysis of COVID 19 cases in 231 countries shows that on average there are around 3,050,828 cases. This number is influenced by countries with high case numbers.
    The median number of cases is 206,897, giving a more typical view of the data. It indicates that half the countries have less cases than this and the other half have 
    more, showing a wide range of case numbers globally. Interestingly, the mode is very low at 9 cases possibly due to data irregularities, countries reporting minimal 
    COVID 19 cases or 'pandas' just taking the minimum of the values, since there's no value appearing more than once. The standard deviation is quite high at about 10,020,789 
    indicating high variation in case numbers between countries. Similarly the variance is also large underscoring this dispersion. The range of case numbers varies greatly 
    from a minimum of 9 to over 111 million cases. This highlights the differences in how severely different countries have been impacted by the pandemic and emphasizes its 
    heterogeneous nature across regions. But also important to mention is, that not all countries have correct data in the source table.
    '''

    # pausing for amount of sleep_time in seconds
    time.sleep(sleep_time)

    # printing mean, median, mode, standard deviation, variance, min and max for total_deaths
    print(f"\nStatistical Analysis for total_deaths:")
    print(f"Mean: {df_covid_stats['total_deaths'].mean()}") # = 31020.048672566372
    print(f"Median: {df_covid_stats['total_deaths'].median()}") # = 2204.5
    print(f"Mode: {df_covid_stats['total_deaths'].mode()[0]}") # = 1.0
    print(f"Standard Deviation: {df_covid_stats['total_deaths'].std()}") # = 110338.9469605656
    print(f"Variance: {df_covid_stats['total_deaths'].var()}") # = 12174683216.366508
    print(f"Minimum: {df_covid_stats['total_deaths'].min()}") # = 1.0
    print(f"Maximum: {df_covid_stats['total_deaths'].max()}") # = 1219392.0
    '''
    The analysis of COVID 19 death tolls all countries reveals some findings. While the average number of deaths stands at around 31,020, this figure can be skewed by countries 
    with high death rates. On the one hand the median of 2,204.5 provides a more typical view showing that half of the countries reported fewer deaths than this and half reported 
    more. Notably the mode indicates one death suggesting that some nations may have reported only one death or possibly have incomplete data. The standard deviation is notably 
    high at 110,339 indicating a dispersion in death counts globally. This is further supported by the variance of 12,174,683,216, both reflecting significant variability and 
    disparities in pandemic impact across different countries. The data ranges from a minimum of one death to a maximum of 1,219,392 deaths illustrating variations in outcomes
    between the most and least affected nations. This analysis highlights impacts of the pandemic on different countries influenced by factors such, as healthcare capacity, 
    demographics and response strategies.
    '''

    # pausing for amount of sleep_time in seconds
    time.sleep(sleep_time)

    # printing mean, median, mode, standard deviation, variance, min and max for total_recovered
    print(f"\nStatistical Analysis for total_recovered:")
    print(f"Mean: {df_covid_stats['total_recovered'].mean()}") # = 32426605.090909091
    print(f"Median: {df_covid_stats['total_recovered'].median()}") # = 58947.0
    print(f"Mode: {df_covid_stats['total_recovered'].mode()[0]}") # = 0.0
    print(f"Standard Deviation: {df_covid_stats['total_recovered'].std()}") # = 9195369.506254409
    print(f"Variance: {df_covid_stats['total_recovered'].var()}") # = 84554820356553.44
    print(f"Minimum: {df_covid_stats['total_recovered'].min()}") # = 0.0
    print(f"Maximum: {df_covid_stats['total_recovered'].max()}") # = 109798081.0
    '''
    The examination of COVID 19 recoveries in all countries shows an average recovery count of around 32,426,605. However this number may be skewed by a countries with very high 
    recovery figures due to a lot of Covid cases. A representative measure is the median at 58,947 recoveries indicating that half of the countries have fewer and half have more 
    than this amount. The frequent value or mode is 0 recoveries, implying that some nations may have reported no recoveries possibly due to incomplete data reporting. The 
    standard deviation is notably high at about 9,195,370 indicating a high range in recovery data among different countries. This significant variation is also evident in the 
    variance at 84,554,820,356,553 signifying substantial differences in recovery figures. The data range from a minimum of 0 to a maximum of 109,798,081 recoveries underscores 
    the contrast in pandemic recovery outcomes between the most and least impacted nations. This broad spectrum highlights the effectiveness and stages of global responses and 
    recovery efforts to the pandemic.
    '''

    # pausing for amount of sleep_time in seconds
    time.sleep(sleep_time)

    # printing mean, median, mode, standard deviation, variance, min and max for total_tests
    print(f"\nStatistical Analysis for total_tests:")
    print(f"Mean: {df_covid_stats['total_tests'].mean()}") # = 30417691.575757574
    print(f"Median: {df_covid_stats['total_tests'].median()}") # = 1690934.0
    print(f"Mode: {df_covid_stats['total_tests'].mode()[0]}") # = 0.0
    print(f"Standard Deviation: {df_covid_stats['total_tests'].std()}") # = 115432158.69029547
    print(f"Variance: {df_covid_stats['total_tests'].var()}") # = 1.3324583259901558e+16
    print(f"Minimum: {df_covid_stats['total_tests'].min()}") # = 0.0
    print(f"Maximum: {df_covid_stats['total_tests'].max()}") # = 1186851502.0
    '''
    The analysis of COVID 19 testing data from all countries reveals variations in testing efforts. The average number of tests conducted stands at around 30,417,691, which is
    significantly higher than the median of 1,690,934 tests. This discrepancy indicates that a few countries with high testing figures are inflating the average while most 
    countries have carried out considerably fewer tests. The absence of reported testing data in some countries (indicated by a mode of 0) may signify gaps in data collection 
    or reporting practices. The high standard deviation of 115,432,158 emphasizes the wide ranging testing disparities among nations. Moreover the variance is notably large 
    highlighting the extensive variation in the data. The range of tests conducted spans from a minimum of zero to a maximum of approximately 1,186,851,502 tests. This broad 
    range underscores the differing capacities and responses to the pandemic across countries. Some nations have been able to conduct testing while others have not. Understanding 
    these disparities is crucial for assessing responses to COVID 19 and preparing for future health emergencies.
    '''

    # pausing for amount of sleep_time in seconds
    time.sleep(sleep_time)

    # printing mean, median, mode, standard deviation, variance, min and max for tot_cases_1m_pop
    print(f"\nStatistical Analysis for tot_cases_1m_pop:")
    print(f"Mean: {df_covid_stats['tot_cases_1m_pop'].mean()}") # = 201191.82683982683
    print(f"Median: {df_covid_stats['tot_cases_1m_pop'].median()}") # = 128681.0
    print(f"Mode: {df_covid_stats['tot_cases_1m_pop'].mode()[0]}") # = 0.0
    print(f"Standard Deviation: {df_covid_stats['tot_cases_1m_pop'].std()}") # = 206118.46995999204
    print(f"Variance: {df_covid_stats['tot_cases_1m_pop'].var()}") # = 42484823658.64814
    print(f"Minimum: {df_covid_stats['tot_cases_1m_pop'].min()}") # = 0.0
    print(f"Maximum: {df_covid_stats['tot_cases_1m_pop'].max()}") # = 771655.0
    '''
    The analysis of COVID 19 cases per 1 million people in all countries shows that the average number of cases is around 201,192, which is notably higher than the median of 128,681. 
    This suggests that there are some countries with high case numbers that are pulling up the average. The common number of cases per million people is zero indicating that some 
    countries either haven't reported any cases or may be lacking data. The standard deviation is quite large at 206,118 cases per million showing significant differences in case numbers
    among different countries. The variance is 42,484,823,658, highlighting the wide range of case numbers across various regions. This variability reflects how differently each country 
    has been impacted by the pandemic due to factors like government measures, healthcare systems and population density. The range of cases per million ranges from zero to a maximum of 
    771,655. This broad range emphasizes the differences in how severely each country has been affected by COVID 19 and provides insights into global health disparities and the effectiveness 
    of public health strategies.
    '''

    # pausing for amount of sleep_time in seconds
    time.sleep(sleep_time)

    # Visualization

    # plotting total cases in histogram
    plt.figure(figsize=(10, 6))
    plt.hist(df_covid_stats['total_cases'], bins=30, color='blue', alpha=0.7)
    plt.title('Histogram of Total COVID-19 Cases')
    plt.xlabel('Total Cases')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()
    '''
    This histogram shows the total of COVID 19 cases in 231 countries divided into 30 sections. On the y axis you can see the frequency, how many countries' total cases are in this specific
    interval. On the x axis you can see the values, the range of all the intervals. The values must be interpreted the following way: 0.2 x 10^8 ==> 20,000,000. Looking at the histogram you
    can see that most of the countries are in the very first interval, which means that almost 200 countries had between 0 and 4,000,000 COVID 19 cases. This once again highlights the differences 
    in how severely different countries have been impacted by the pandemic and emphasizes its heterogeneous nature across regions. Moreover, what goes into consideration is that countries with
    smaller populations obviously have a smaller amount of total cases. But also important to mention is, that not all countries have correct data in the source table. Besides that there's one
    outlier with 100,000,000+ Covid 19 cases, which is the USA. This plot emphasizes very well, how severely the USA has been impacted by the pandemic, showing the gap in total cases between
    them and the next country, which is at below 50,000,000 cases.
    '''

    # plotting total recovered in histogram
    plt.figure(figsize=(10, 6))
    plt.hist(df_covid_stats['total_recovered'], bins=30, color='green', alpha=0.7)
    plt.title('Histogram of Total COVID-19 Recoveries')
    plt.xlabel('Total Recovered')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()
    '''
    This histogram shows the total of COVID 19 recoveries in all countries divided into 30 sections. On the y axis you can see the frequency, how many countries' total recoveries are in this 
    specific interval. On the x axis you can see the values, the range of all the intervals. The values must be interpreted the following way: 0.2 x 10^8 ==> 20,000,000. This histogram looks very similar
    to the one before. Looking at it you can see again, that most of the countries are in the very first interval, which means that almost 200 countries had between 0 and 4,000,000 COVID 19 recoveries. Also
    you can see one outlier again, which is the USA with 100,000,000+ recoveries. Comparing this histogram to the histogram before with the total cases we can draw interesting conclusions. Even though we've 
    had a lot of cases all around the world, we can see that the recovery numbers are very high as well. They are definitely not as high as the total case numbers, what shows that there's still a 
    significant amount of people that didn't make it through this disease. But overall compared to the total cases we've had a lot of recoveries. Of course this came with a massive strain on 
    the health systems all over the world, but in the end of the day these are good numbers.
    '''

    # boxplot for cases per million in boxplot
    plt.figure(figsize=(10, 6))
    plt.boxplot(df_covid_stats['tot_cases_1m_pop'], vert=False)
    plt.title('Boxplot of Total Cases per 1 Million Population')
    plt.xlabel('Cases per 1 Million')
    plt.grid(True)
    plt.show()
    '''
    This boxplot shows the total of COVID 19 cases per 1 million population. On the x axis you can see number of total cases per one million population, stretching from 0 to 800,000. We see the median at about
    130,000, what implies that 50% of the countries had higher and 50% of the countries lower numbers than that. The minimum shows at 0 and the maximum at about 770,000. The interquartile range stretches from
    about 20,000 (first quartile) to about 330,000 (third quartile), showing the inner 50% of the data. This shows us that most of the data is at about half of the maximum. We can also see that 50 percent of the
    data is below approximately 130,000, which is very low compared to the maximum. This visualization uses relative numbers. This gives a little more context to the numbers and helps to assess the severity for
    each country. So you can see that in most countries only around one in ten to one in three was infected. This puts the high total cases value in the USA into perspective, as statistically 'not even' every 
    person was infected here. Of course, it must again be taken into account that the data was probably not recorded one hundred percent accurately.
    '''

    # success message
    print("\nVisualizations successfully plotted.")
    time.sleep(sleep_time)

    # printing process time
    print(f'\nprocess finished -- {time.time()-start}s --\n')