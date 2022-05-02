import time
import pandas as pd
import numpy as np
from pandas.io.parsers import read_csv
from datetime import timedelta as td

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str.lower(input('Which city would you like to get data from? Chicago, New York City or Washington?: '))
        if city.lower() not in ('chicago', 'washington', 'new york city'):
            print('Sorry, that is not a valid city. Try again!')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = str.lower(input('Should the data be for all months or a specific month(January to June)?  '))
        if month.lower() not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print('Sorry, that is not a valid month. Try again!')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str.lower(input('Which day of the week? '))
        if day.title() not in ('All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'):
            print('Sorry, that is not a valid day. Try again!')
        else:
            break
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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # extract hour from Start Time to create a new column
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':


        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_statistics(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month of travel is', df['month'].mode()[0])

    # display the most common day of week
    print('The most common day of travel is', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('The most common hour of travel is', df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is', df['Start Station'].mode()[0], 'with a count of', len(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used end station is', df['End Station'].mode()[0], 'with a count of', len(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['combined_station'] = df['Start Station'] + ' to ' + df['End Station']
    print('The most frequent trip is ', df['combined_station'].mode()[0], 'with a count of', len(df['combined_station'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time, taking the trip duration in the data to be seconds
    print('The total travel time is: ', td(seconds= df['Trip Duration'].sum().item()))

    # display mean travel time taking the trip duration in the data to be seconds
    print('The average trip duration is: ', td(seconds= df['Trip Duration'].mean().item()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The categories of users and the count of each are as follow\n', df['User Type'].value_counts())

    # Display counts of gender
    """Washington does not have gender and birth year data.
    Using try to avoid break of code"""
    try:
        print('\nThe number of users for each gender are\n', df['Gender'].value_counts())

    except KeyError:
        # Display this for city(s) without gender data
        print('\nNo gender data available for this city')


    # Display earliest, most recent, and most common year of birth
    try:
        # Display earliest year of birth
        print('\nThe earliest year of birth is', int(df['Birth Year'].min()))

        # Display most recent year of birth
        print('The most recent year of birth is', int(df['Birth Year'].max()))

        # Display the ost common year of birth
        print('Most of the users were born in the year', int(df['Birth Year'].mode()[0]))

    except KeyError:
        # Display this for city(s) without birth year data
        print('Birth year data is unavailable for this city')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw(df):
    """Displays 5 rows of the dataframe used for the analysis"""

    start_loc = 0
    end_loc = 5
    while True:
        user_input = str.lower(input('Would you like to see 5 rows of raw data? (Yes/No):\n'))
        if user_input == 'yes' and end_loc < len(df):
            print(df.iloc[start_loc:end_loc])
            while True:
                user_input = str.lower(input('Would you like to see the next 5 rows of raw data? (Yes/No):\n'))
                if user_input == 'yes' and end_loc < len(df):
                    print(df.iloc[start_loc + 5: end_loc + 5])
                    start_loc += 5
                    end_loc += 5
                elif user_input == 'no':
                    print('That is the end of code')
                    break
            break
        elif user_input == 'no':
            print('That is the end of the code')
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
