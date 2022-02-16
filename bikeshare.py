import time
import calendar
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
     # get user input for city (chicago, new york city, washington).    
    temp = 1 
    Select_phrase = 'Hello! Let\'s explore some US bikeshare data!\nWould you like to see data for Chicago, New York City or Washington?\n'   
    while temp == 1:
        city = input(Select_phrase).lower()
        for key in CITY_DATA.keys():
            if city == key:
                temp = 0
        Select_phrase = 'Incorrect choice, please select data for Chicago, New York City or Washington?\n'

    # Display raw data or not
    df = pd.read_csv(CITY_DATA[city]) 
    step = 0
    show_Y_N = input('Would you like to see 5 rows of raw data? Enter yes or no to go on and explore US bikeshare data.\n')
    No_rows = len(df.index)

    while True:        
        if show_Y_N.lower() != 'yes':
            break
        elif step > No_rows:
            print('End of file!')
            break
        else:
            print(df.iloc[0+step:5+step])
            step += 5
            show_Y_N = input('Would you like to see another 5 rows of raw data? Enter yes or no to continue?\n')


    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february','march','april','may','june']
    temp = 1 
    Select_phrase = 'Select a month January, February,...June or All\n'  
    while temp == 1:
        month = input(Select_phrase).lower()
        for item in range(len(months)):
            if month == months[item]:
                temp = 0
        Select_phrase = 'Incorrect choice, select a month January, February,...June or All\n'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']
    temp = 1 
    Select_phrase = 'Select a day Monday, Tuesday,...,Sunday or All\n'  
    while temp == 1:
        day = input(Select_phrase).lower()
        for item in range(len(days)):
            if day == days[item]:
                temp = 0
        Select_phrase = 'Incorrect choice, select a day Monday, Tuesday,...,Sunday or All\n'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # read file
    df = pd.read_csv(CITY_DATA[city])   
    
    # add columns month, day_of_week, start hour and Start_End_station
    # filter if != all  
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour
    df['Start_End_Station'] = 'Start Station: ' + df['Start Station'] + ', End Station: ' + df['End Station']
  
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month:', calendar.month_name[df['month'].mode()[0]])
    
    # display the most common day of week
    print('Most common day of week:', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('Most common start hour:', df['Start Hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most commonly used end station:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('Most frequent combination of start station and end station trip: \n' + df['Start_End_Station'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    "Displays statistics on the total and average trip duration."

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time:', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean travel time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types:')
    print(df['User Type'].value_counts().to_string())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nCounts of gender:')
        print(df['Gender'].value_counts().to_string())
    else:
        print('\nNo gender statistics for ' + city.title())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:        
        print('\nEarliest year of birth:' , int(np.nanmin(df['Birth Year'])))
        print('Most recent year of birth:' , int(np.nanmax(df['Birth Year'])))        
        print('Most common year of birth:' , int(df['Birth Year'].mode()[0]))       
    else:
        print('No birth year statistics for ' + city.title())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
